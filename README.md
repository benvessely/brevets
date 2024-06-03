# Project 6: Brevet time calculator service

Addition of a RESTful API on top of the database and website functionality from Projects 4 and 5.

## Author

Finalized by Ben Vessely; initial code by UO CS faculty.

## Running the program
The main code is within the brevets_proj6 subdirectory of the main proj6-rest-vessely repository. Simply enter this subdirectory and run docker-compose up --build to get the program running.  

## Consumer Program
It is getting late on Friday night, and I am having weird issues with getting the JSON data into my php program from the API endpoint. I tried using the file_get_contents() function and using cURL, but in both cases, I was getting None from the API even though I wasn't getting a cURL error. I performed a bunch of debugging/troubleshooting steps with the help of Copilot, but none of them worked; I will therefore skip the consumer program for now. The API should still be testable just by providing the desired additions to localhost:5000 in your browser, of course. 

## API endpoints

There are many endpoints that were added to the API in this project. Change the values for host and port according to your machine, and use the web browser to check the results.

* You will design RESTful service to expose what is stored in MongoDB. Specifically, you'll use the boilerplate given in DockerRestAPI folder, and create the following three basic APIs:
    * `http://<host:port>/listAll` should return all open and close times in the database
    * `http://<host:port>/listOpenOnly` should return open times only
    * `http://<host:port>/listCloseOnly` should return close times only

* You will also design two different representations: one in csv and one in json. For the above three basic APIs, JSON should be your default representation. 
    * `http://<host:port>/listAll/csv` should return all open and close times in CSV format
    * `http://<host:port>/listOpenOnly/csv` should return open times only in CSV format
    * `http://<host:port>/listCloseOnly/csv` should return close times only in CSV format

    * `http://<host:port>/listAll/json` should return all open and close times in JSON format
    * `http://<host:port>/listOpenOnly/json` should return open times only in JSON format
    * `http://<host:port>/listCloseOnly/json` should return close times only in JSON format

* You will also add a query parameter to get top "k" open and close times. For examples, see below.

    * `http://<host:port>/listOpenOnly/csv?top=3` should return top 3 open times only (in ascending order) in CSV format 
    * `http://<host:port>/listOpenOnly/json?top=5` should return top 5 open times only (in ascending order) in JSON format
    * `http://<host:port>/listCloseOnly/csv?top=6` should return top 5 close times only (in ascending order) in CSV format
    * `http://<host:port>/listCloseOnly/json?top=4` should return top 4 close times only (in ascending order) in JSON format


