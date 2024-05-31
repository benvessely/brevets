""" Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import Flask, redirect, url_for, request, render_template, flash
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import logging
from pymongo import MongoClient
import os
from bson.json_util import dumps, loads 
from flask_restful import Resource, Api


###
# Globals
###
app = flask.Flask(__name__)
api = Api(app)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY


###
# Setup Database
###
client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.controlsdb

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brevet_dist = request.args.get('brevet_dist', type=int)
    begin_time = request.args.get('begin_time') 
    begin_date = request.args.get('begin_date')
    # app.logger.debug(f"begin_time: {begin_time}") 
    # app.logger.debug(f"begin_date: {begin_date}") 
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    begin_datetime_str = f"{begin_date} {begin_time}"
    begin_datetime = arrow.get(begin_datetime_str, 'YYYY-MM-DD HH:mm')
    iso_begin_datetime = begin_datetime.isoformat()
    # app.logger.debug(f"begin_datetime = {begin_datetime}")
    # app.logger.debug(f"iso_begin_datetime = {iso_begin_datetime}")
    open_time = acp_times.open_time(km, brevet_dist, iso_begin_datetime)
    close_time = acp_times.close_time(km, brevet_dist, iso_begin_datetime)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


@app.route("/submit", methods=['POST'])
def submit(): 
    app.logger.debug("Entering submit()")
    form = request.form
    app.logger.debug(f"request.form = {form}")

    miles = request.form.getlist('miles') 
    kms = request.form.getlist('km')
    locations = request.form.getlist('location') 
    open_times = request.form.getlist('open') 
    close_times = request.form.getlist('close')  
    app.logger.debug(f"miles = {miles}")
    app.logger.debug(f"kms = {kms}")
    app.logger.debug(f"locations = {locations}")
    app.logger.debug(f"open_times = {open_times}")
    app.logger.debug(f"locations = {close_times}")
    
    if kms[0] == '': 
        flask.flash("Error: Add at least one control to the table before submitting")

    i = 0 
    while kms[i] != '': 

        # Get ith row of the db ready, as a document, to be inputted to db 
        new_doc = { 
            'mile': miles[i],
            'km': kms[i],
            'location': locations[i],
            'open': open_times[i],
            'close': close_times[i]
        }

        # Input stuff into database here 
        db.controls.insert_one(new_doc)
        i += 1

    flask.flash("Data from table posted to database") 
    return redirect(url_for('index'))


@app.route("/display", methods=['GET'])
def display(): 
    app.logger.debug("Entered display()")
    _controls = db.controls.find()
    controls = [control for control in _controls]
    if len(controls) == 0: 
        flask.flash("Error: Database empty; nothing to display")
        return redirect(url_for('index'))
    else:
        return render_template("display.html", controls=loads(dumps(controls)))


###
# Flask-Restful API starts here
###


# Helper function to retrieve all open, close times from "controls" collection.
# Returns a python dict with these times.
def get_times(): 
    collection = db.controls
    times = { "times": [] } 
    for open_close_time in collection.find({}, {'_id': 0, \
                                                'open': 1, 'close': 1 }):
        times["times"].append(open_close_time)
    app.logger.debug(f"Open and close times from db = {times}")
    return times


# Given a JSON structure, will return the structure in csv format as a string
def csv_convert(times, get_open, get_close): 
    labels = ""
    times_str = ""
    for element_count in range(len(times["times"])):
        if get_open: 
            labels += f"control{element_count + 1}/open, "
            times_str += f"{times['times'][element_count]['open']}, "
        if get_close: 
            labels += f"control{element_count + 1}/close, " 
            times_str += f"{times['times'][element_count]['close']}, "
    # Remove final trailing comma and space
    labels = labels[:-2]
    times_str = times_str[:-2]
    combined = labels + "\n" + times_str
    app.logger.debug(f"CSV string of labels is {labels}")
    app.logger.debug(f"CSV string of times is {times_str}") 
    app.logger.debug(f"Combined CSV string with labels and times is {combined}")
    return combined   


class ListAll(Resource): 
    def get(self, data_format='json'): 
        times = get_times()
        if data_format == 'csv': 
            times_csv = csv_convert(times, get_open=True, get_close=True) 
            return times_csv 
        else: 
            return flask.jsonify(times) 
        

class ListOpenOnly(Resource): 
    def get(self, data_format='json'): 
        times = get_times()
        if data_format == 'csv': 
            times_csv = csv_convert(times, get_open=True, get_close=False) 
            return times_csv 
        else: 
            for dct in times["times"]: 
                del dct["close"]
            return flask.jsonify(times) 


class ListCloseOnly(Resource): 
    def get(self, data_format='json'): 
        times = get_times()
        if data_format == 'csv': 
            times_csv = csv_convert(times, get_open=False, get_close=True) 
            return times_csv 
        else:
            for dct in times["times"]: 
                del dct["open"] 
            return flask.jsonify(times)  

api.add_resource(ListAll, '/listAll', '/listAll/<string:data_format>')
api.add_resource(ListOpenOnly, '/listOpenOnly', '/listOpenOnly/<string:data_format>')
api.add_resource(ListCloseOnly, '/listCloseOnly', \
                 '/listCloseOnly/<string:data_format>')

""" 
Questions for Nate: 
Is having many URIs for one resource and then parsing the URI a good approach here? 
Should my data have a label for the  brevet distance or anything? Does my JSON look right? 
Should I return the csv as another file or something? If not, what does it mean to expose a CSV file for use by an API? 

Notes: 
Can just parse the URI like I was thinking all within the single method 
Only need open and close times. Can be useful to have the other stuff but not needed 
I can return the csv as a file or as a string. Seems easier to me to just deal with it as a string
""" 


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
