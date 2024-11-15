# ACP Brevet Control Times Calculator

This project is a reimplementation of the RUSA ACP controle time calculator for brevet bike races, found [here](https://rusa.org/octime_acp.html). In the development process, I learned a lot  about Flask, Flask-RESTful for API functionality, MongoDB, Docker, and AJAX, as well as how these technologies can be applied to a full-stack application. 

## Credits

By Ben Vessely (bvessely at uoregon dot edu). Credit to Michal Young, Ziyad Alsaeed, and other UO CS academic staff for the starter code. 

## Installation and Usage
The github repository for this project can be cloned via 
```bash
git clone https://github.com/benvessely/brevets.git
``` 

To start the program, simply enter the `brevets` subdirectory and run 
```bash
docker-compose up --build
```
to get the program running. In your browser, `localhost:5000/index` should show the index page for the calculator. The API endpoints can be accessed via `localhost:5000/{endpoint}`, where the possible endpoints are described below. There is also a basic PHP consumer program to consume the API services, which can be found at `localhost:5001`. Note that the port numbers shown here can be changed at any time within the `brevets/docker-compose.yml` file.

## About Brevet Races

Brevets are long-distance bike races with checkpoints, called "controles" (from here on, we will remove the "e" and simply refer to them as controls or control points). In these races, riders do not compete against each other, nor do riders attempt to get their best time overall. Rather, riders complete the race successfully if they make it to all of the controls within a certain window of time. To calculate this window of time, there is a pre-determined algorithm that outputs the open and close times for any given control based on its distance. 

## Algorithm for Control Open and Close Times
The algorithm for calculating the opening and closing times for each control is calculated based on a minimum and maximum speed, respectively, that the riders must keep their average speed between. We will refer to the following table in our explanation:

| Interval (km)         | Minimum Speed (km/hr) | Maximum Speed (km/hr) |
| --------------------- | --------------------- | --------------------- |
| 0 - 200               | 15                    | 34                    |
| 200 - 400             | 15                    | 32                    |
| 400 - 600             | 15                    | 30                    |
| 600 - 1000            | 11.428                | 28                    |
| 1000 - 1300           | 13.333                | 26                    |

We will take a look at the calculation for the time time for a control, as the open time calculation is analogous. In calculating close time, one can intuitively think that on each interval, the rider must not go any slower, on average, than the minimum speed on that interval. 

The formal calculation for the close time is 
$$ \text{Open time} = \sum_{\text{all interval}} 
    \frac{\text{amount of control distance in interval}}
    {\text{minimum speed on that interval}}  $$
As an example, for a control at 200km, we would have a close time of
$$ 200/15 + 0 / 15 + 0 / 15 + 0 / 11.428 + 0 / 13.333 \approx 13.33 \text{ hours} . $$
As another example, consider a control at 1100km. The close time for this control would be 
$$ 200/15 + 200/15 + 200/15 + 400/11.428 + 100/13.333 \approx 82.50 \text{ hours} . $$ 

The open time calculation is analogous---we simply replace the maximum speed on each interval by the minimum speed, giving
$$ \text{Close time} = \sum_{\text{all intervals}} 
    \frac{\text{amount of control distance in interval}} 
    {\text{maximum speed on that interval}} 
$$

Note that these calculations return times in hours, but we can convert the part after the decimal point to minutes by taking the numbers after the decimal point and multiplying by 60, and then rounding the result to the nearest integer. 

It is helpful to note that the logic for these calculations is quite similar to the workings of tax brackets. As an example (with arbitrary rates), if someone earned $40,000, the first $10,000 are taxed at a rate of 10%, the next $15,000 at a rate of 12%, and the last $15,000 at a rate of 15%. The taxes that this person owes are then 
$$ \$10,000 \cdot 0.10 + \$15,000 \cdot 0.12 + \$15,000 \cdot 0.15 = \$5,050. $$ 

As an additional complication, for the brevet (finish line) timing, the following close times are used (in hours and minutes, HH:MM): 13:30 for 200km, 20:00 for 300km, 27:00 for 400km, 40:00 for 600km, 75:00 for 1000km. Notice that these times are different than those calculated in the previously stated algorithm. In another strange case, if a control is greater than or equal to the brevet distance, simply take the close time for the control to be equal to the special close time for the brevet.

The algorithm for calculating control times is also described 
[here](https://rusa.org/pages/acp-brevet-control-times-calculator), and additional background information on the details of brevets and the algorithm is given [here](https://rusa.org/pages/rulesForRiders). There are some small discrepencies between the algorithm specifications described at the "Rules for Riders" site and the calculator, in which case we chose to mimic the behavior of the  calculator.

There are some small discrepencies between the algorithm specifications described at the "Rules for Riders" site and the calculator, in which case we chose to mimic the behavior of the [calculator](https://rusa.org/octime_acp.html).


## AJAX for Autofill of Open and Close Time 
For our calculator, the user will input a brevet distance, start date, and start time at the top of the page. Then, after the user inputs a control distance into either the miles or kilometers box in any row of the table below, the open and close times for that control will be automatically populated, as will the remaining mile/kilometer box. This is implemented using AJAX to increase the reactivity of the page.

## Viable Control Distances
The distance for a control should be any value between 0 and 1.2 times the brevet distance. More specifically, negative distances and control distance more than 20% past the brevet distance will throw an error, while control distances between 0% and 20% past the brevet distance will simply be treated as if it were the same as the brevet distance. 

## MongoDB Database Functionality
The table on the client side interacts with MongoDB via two buttons. The first is the "Submit" button, which sends an HTTP POST request to enter the data from the table into a database, while the "Display" button sends an HTTP GET request to get the data from the database and display it on a new page. 

## Test Cases for MongoDB

Test Case 1 (Trivial): Just after starting the application, press display. The database is empty, so a message should display below the Display button saying "Error: Database empty; nothing to display" 

Test Case 2 (Trivial): Leave the table totally empty, then press submit. This should give an error saying "Error: Add at least one control to the table before submitting" 

Test Case 3: Leaving the distance and begins at information unchanged from the initial load of the page, enter 0 in the first km box, 50 in the box below it, 60 into the box below 50, then 199, then 200, and then 210. Click anywhere on the page that's not in the table, then press submit. A message should pop up below the buttons saying "Data from table posted to database". 

Test Case 4: Immediately after running Test Case 3, press the display button. The control times corresponding to controls at 0, 50, 60, 199, 200, and 210 should show up in a table on a new page.

## API

As part of the same Flask application used for our main calculator functionality, I created an API using Flask-RESTful that exposes the data stored in MongoDB. Again, we will use `localhost:5000`, but the port can be changed at any time.

The basic endpoints for accessing the data are shown below. 
    * `http://<host:port>/listAll` should return all open and close times in the database
    * `http://<host:port>/listOpenOnly` should return open times only
    * `http://<host:port>/listCloseOnly` should return close times only

* I also designed two different representations of the data, one in JSON and one in CSV. For the above three basic APIs, JSON is the default representation.
    * `http://<host:port>/listAll/csv` should return all open and close times in CSV format
    * `http://<host:port>/listOpenOnly/csv` should return open times only in CSV format
    * `http://<host:port>/listCloseOnly/csv` should return close times only in CSV format

    * `http://<host:port>/listAll/json` should return all open and close times in JSON format
    * `http://<host:port>/listOpenOnly/json` should return open times only in JSON format
    * `http://<host:port>/listCloseOnly/json` should return close times only in JSON format

* There is also a query paramter to get the top "k" open and close times. For example, 

    * `http://<host:port>/listOpenOnly/csv?top=3` should return top 3 open times only (in ascending order) in CSV format 
    * `http://<host:port>/listOpenOnly/json?top=5` should return top 5 open times only (in ascending order) in JSON format
    * `http://<host:port>/listCloseOnly/csv?top=6` should return top 5 close times only (in ascending order) in CSV format
    * `http://<host:port>/listCloseOnly/json?top=4` should return top 4 close times only (in ascending order) in JSON format


## Consumer Program 
The PHP consumer program will be automatically created via the `docker-compose up` command, and can be accessed at `localhost:5001` (or any port chosen in `docker-compose.yml`). 