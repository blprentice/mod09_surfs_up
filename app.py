# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Set up the database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect database into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Session (link) from Python to DB
session = Session(engine)

# Set up Flask
app = Flask(__name__)

# Define the welcome route
@app.route("/")

# Add routing information for each of the other routes
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!\n
    Available Routes:\n
    /api/v1.0/precipitation\n
    /api/v1.0/stations\n
    /api/v1.0/tobs\n
    /api/v1.0/temp/start/end
    ''')

# Create precipitation route
@app.route("/api/v1.0/precipitation")

def precipitation():

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    
    precip = {date: prcp for date, prcp in precipitation}
        
    return jsonify(precip)

# Create stations route
@app.route("/api/v1.0/stations")

def stations():

    # Create query allowing us to get all the stations in database
    results = session.query(Station.station).all()

    # Unravel results into one-dimensional array, then convert unraveled results into a list
    stations = list(np.ravel(results))
    
    # jsonify the list and return as JSON
    return jsonify(stations=stations)

# Create temperature observations (tobs) route
@app.route("/api/v1.0/tobs")

# Create function
def temp_monthly():

    # Calculate the date one year ago from last date in db
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the primary station for all temp obs from previous year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter (Measurement.date >= prev_year).all()
    
    # Unravel results into 1D array and convert to list
    temps = list(np.ravel(results))

    # jsonify the list and return as JSON
    return jsonify(temps=temps)

# Create statistics route
@app.route("/api/v1.0/temp/<start>")

@app.route("/api/v1.0/temp/<start>/<end>")

# Create function, adding parameters to the function
def stats(start=None, end=None):

    # Create a query to select min, avg, max temps from DB
    # Create list
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # Add if not statement to determine starting and ending date
    if not end:
        # Query the database using sel list (asterisk (*) indicates there will be multiple results for query - min, avg, max temps)
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        
        # Unravel results into 1D array and convert to list
        temps = list(np.ravel(results))

        return jsonify(temps=temps)
    
    # Query to calculate temp min, avg, and max with start and end dates
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    temps = list(np.ravel(results))
    
    # jsonify the list and return as JSON
    return jsonify(temps=temps)
