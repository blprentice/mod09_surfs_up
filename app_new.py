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

    Welcome to the Claimate Analysis API!

    Available Routes:

    /api/v1.0/precipitation

    /api/v1.0/stations

    /api/v1.0/tobs

    /api/v1.0/temp/start/end

    ''')
