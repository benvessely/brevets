import arrow 
import typing

TEST_START_TIME = arrow.get('2024-05-17 00:00:00', 'YYYY-MM-DD HH:mm:ss')

def calc_time_tst(hours_to_add: int, minutes_to_add: int, start_time: str):
    """ 
    start_time should be an isoformat string
    """ 
    # Initialize arw_time to be an arrow object for same date/time as start_time
    arw_time = arrow.get(start_time)

    arw_time = arw_time.shift(hours=+hours_to_add)
    arw_time = arw_time.shift(minutes=+minutes_to_add)

    return arw_time.isoformat()

# test1 = calc_time_tst(5, 53, TEST_START_TIME)
# print(f"MY DEBUG: calc_time_tst(5, 53, TEST_START_TIME = {test1})")



