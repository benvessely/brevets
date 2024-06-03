"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

# Each element from the table is a tuple of four elements. The first and second 
# attributes of the tuple are the lower and upper bounds, respectively, of an
# interval (km) on which minimum and maximum speeds will be defined. The third 
# attribute of the tuple is the minimum speed (km/hr) on that interval, and the
# fourth attribute is the maximum speed (km/hr) on that interval. 
 
SPEEDS = [(0, 200, 15, 34), (200, 400, 15, 32), (400, 600, 15, 30), 
          (600, 1000, 11.428, 28), (1000, 1300, 13.333, 26)] 

BREVET_TIMES = { 200: (5 + 33/60, 13 + 30/60), 300: (9, 20), 400: (12 + 8/60, 27), 
                600: (18 + 48/60, 40), 1000: (39, 75) } 


#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    # print(f"MY DEBUG: brevet_start_time = {brevet_start_time}")
    arw_begin = arrow.get(brevet_start_time) 

    year = arw_begin.year
    month = arw_begin.month
    day = arw_begin.day
    hour = arw_begin.hour
    minute = arw_begin.minute

    hour_decimal = hour + minute / 60 
    time_delta_hours = time_to_open(control_dist_km, brevet_dist_km)

    # If we got an error tuple, return that tuple 
    if isinstance(time_delta_hours, list): 
        return time_delta_hours
  
    time_delta_mins = int(round(time_delta_hours * 60))
    open_time = arw_begin.shift(minutes=+time_delta_mins) 
    print(f"MY DEBUG: Open time is {open_time}") 

    return open_time.isoformat() 



'''
Thinking: 

Okay so how is this going to work. I will calculate the opening time for the 
control by splitting it up into components based on the specified intervals.
If the control distance is within 15 miles of the brevet distance, I will just 
calculate the time for that control as if it was at the brevet distance. 
This is true even if there are multiple controls within 15km of the brevet
distance. 

I will also have to factor inthat I might overrun on incremdent hours, days,  
months, or years in my calculation. If so, I will need to increment those 
counters correspondingly. I need to make sure I'm watching out for weird edge 
cases here. 
'''

def time_to_open(control_dist_km, brevet_dist_km):
    if control_dist_km < 0:
        return [False, "Brevet distance must be non-negative."]
    # If control is more than 20% past the brevet, we return an error
    if control_dist_km > (brevet_dist_km * 1.2): 
        return [False, "Control distance must not be more than 20% larger "
                         + "than brevet distance."]

    # This code is actually not used for open times, as for open times the 
    # calculator just uses the algorithm time, not the special table time 
    # if brevet_dist_km <= control_dist_km and \
    #         control_dist_km <= (brevet_dist_km * 1.2): 
    #     print(f"MY DEBUG: Control within 20% after brevet" + 
    #           f" returning {BREVET_TIMES[brevet_dist_km][0]}")
    #     return BREVET_TIMES[brevet_dist_km][0]
    
    # If control is within 20% after the brevet, just treat the control 
    # distance as equal to the brevet distance. Open times for brevet 
    # distance are dealt with via the algorithm, not via the special cases
    # detailed in Article 9 of the Rules for Riders page 
    if brevet_dist_km <= control_dist_km and \
            control_dist_km <= (brevet_dist_km * 1.2): 
        control_dist_km = brevet_dist_km 

    time_delta = 0 
    interval_num = 0
    remaining_dist = control_dist_km
    # print(f"MY DEBUG: control_dist_km = {control_dist_km}, " + 
    #         f"brevet_dist_km = {brevet_dist_km}")
    # print(f"\nMY DEBUG: Entering while loop")
    while remaining_dist > 0:
        # print(f"MY DEBUG: remaining_dist = {remaining_dist}, " + 
        #        f"interval_num = {interval_num}, time_delta = {time_delta}") #DB 
        interval_size = SPEEDS[interval_num][1] - SPEEDS[interval_num][0]
        # Use max in case remaining_dist is shorter than the considered interval
        dist_in_interval =  min(interval_size, remaining_dist)
        max_speed = SPEEDS[interval_num][3]
        # print(f"MY DEBUG: dist_in_interval = {dist_in_interval}, " + 
        #         f"max_speed = {max_speed}") #DB
        time_delta += dist_in_interval / max_speed
        # Decrease remaining_dist so that we can consider the next speed interval
        remaining_dist -= interval_size
        interval_num += 1
        # print(f"MY DEBUG: remaining_dist = {remaining_dist}, " + 
        #         f" time_delta = {time_delta}") #DB 


    # print(f"MY DEBUG: While loop done, output of time_to_open: {time_delta}\n") #DB 

    return time_delta 


''' 
What special cases am I going to have to consider here? Distance negative, 
control greater than brevet, control at 0 (works I think), control within 10 miles of 
brevet distance. 
''' 



def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    print(f"MY DEBUG: brevet_start_time = {brevet_start_time}")
    arw_begin = arrow.get(brevet_start_time) 

    year = arw_begin.year
    month = arw_begin.month
    day = arw_begin.day
    hour = arw_begin.hour
    minute = arw_begin.minute

    hour_decimal = hour + minute / 60 
    time_delta_hours = time_to_close(control_dist_km, brevet_dist_km)

    # If we got an error tuple, return that tuple 
    if isinstance(time_delta_hours, list): 
        return time_delta_hours

    time_delta_mins = int(round(time_delta_hours * 60))
    close_time = arw_begin.shift(minutes=+time_delta_mins) 
    print(f"MY DEBUG: Close time is {close_time}") 

    return close_time.isoformat() 


def time_to_close(control_dist_km, brevet_dist_km):
    if control_dist_km < 0:
        return [False, "Brevet distance must be non-negative."]
    if control_dist_km > (brevet_dist_km * 1.2): 
        return [False, "Control distance must not be more than 20% larger "
                         + "than brevet distance."]

    # If control within 20% after brevet finish (including brevet finish), treat control distance as if it were brevet distance
    if brevet_dist_km <= control_dist_km and \
            control_dist_km <= (brevet_dist_km * 1.2): 
        print(f"MY DEBUG: Control within 20% after brevet" + 
              f" returning {BREVET_TIMES[brevet_dist_km][1]}")
        return BREVET_TIMES[brevet_dist_km][1]
    
    time_delta = 0 
    interval_num = 0
    remaining_dist = control_dist_km
    # print(f"MY DEBUG: control_dist_km = {control_dist_km}, " + 
    #         f"brevet_dist_km = {brevet_dist_km}")
    # print(f"\nMY DEBUG: Entering while loop")
    while remaining_dist > 0:
        # print(f"MY DEBUG: remaining_dist = {remaining_dist}, " + 
        #        f"interval_num = {interval_num}, time_delta = {time_delta}") #DB 
        interval_size = SPEEDS[interval_num][1] - SPEEDS[interval_num][0]
        # Use max in case remaining_dist is shorter than the considered interval
        dist_in_interval =  min(interval_size, remaining_dist)
        max_speed = SPEEDS[interval_num][2]
        # print(f"MY DEBUG: dist_in_interval = {dist_in_interval}, " + 
        #        f"max_speed = {max_speed}") #DB
        time_delta += dist_in_interval / max_speed
        # Decrease remaining_dist so that we can consider the next speed interval
        remaining_dist -= interval_size
        interval_num += 1
        # print(f"MY DEBUG: remaining_dist = {remaining_dist}, " + 
        #         f" time_delta = {time_delta}") #DB 

    print(f"MY DEBUG: While loop done, output of time_to_close: {time_delta}\n") #DB 
    return time_delta 



'''
Notes from Meeting: There will be tests for weird cases. What if control point is 0. What if control point is after brevet distance? 

Basically just put handling of ambiguity in the README so he knows how we are interpreting this. 

print statements do not work within docker, so I would have to just run the app without docker to get that to work 

''' 
