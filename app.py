# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Set up the Database
# Create function allows access to SQLite database file
engine = create_engine("sqlite:///hawaii.sqlite")
# Reflect database into classes
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Creates session link from Python to SQLite database
session = Session(engine)
# Set up Flask app, all routes go after this code
app = Flask(__name__)

# Example of app name variable
# import app
# print("example __name__ = %s", __name__)
# if __name__ == "__main__":
#     print("example is being run directly.")
# else:
#     print("example is being imported")

# Define the welcome route
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# 9.5.3 Precipitation Route
@app.route("/api/v1.0/precipitation")

# Use Jsonify() to converts the dictionary to a JSON file

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# 9.5.4 Stations Route
# define the route and route name
@app.route("/api/v1.0/stations")

# Create a new function
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# 9.5.5 Monthly Temperature Route
# Define the route and route name
@app.route("/api/v1.0/tobs")

# Create a new function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# 9.5.6 Statisics Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

