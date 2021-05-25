import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

########## Home Page ########## 

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to Climate App<br/>"
        f"Available Routes:<br/>"
        f"Precipitation Data: /api/v1.0/precipitation<br/>"
        f"Stations List: /api/v1.0/stations<br/>"
        f"Temperature Observation for the most active station: /api/v1.0/tobs<br/>"
        f"Enter a Starting Date: /api/v1.0/yyyy-mm-dd to get the TMIN, TAVG and TMAX for all dates greater and equal to the Starting Date<br/>"
        f"Enter a Starting and Ending Date: /api/v1.0/yyyy-mm-dd/yyyy-mm-dd to get the TMIN, TAVG and TMAX for the dates between the Start and End dates inclusives"
    )


########## Precipitation ##########

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query precipitation
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()

    session.close()

    # Convert the query results to a dictionary using date as the key and prcp as the value.
    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)


########## Stations ##########

@app.route("/api/v1.0/stations")
def stations():
    # Create session from Python to the DB
    session = Session(engine)

    # Query station
    stations_list = session.query(Station.name, Station.station).all()

    session.close()
    

    return jsonify(stations_list)


########## Temperature Observations ##########

@app.route("/api/v1.0/tobs")
def tobs():
    # Create session from Python to the DB
    session = Session(engine)

    # Query tobs
    tobs_query = session.query(Station.station, Station.name, Measurement.station, Measurement.date, Measurement.tobs).filter(Station.station == Measurement.station).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()

    session.close()

    return jsonify(tobs_query)


########## Start Route ##########

@app.route("/api/v1.0/<start>")
def start(start):
    # Create session from Python to the DB
    session = Session(engine)

    # Query Start Date
    start_date_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    # Convert the query results to a dictionary
    start_date_list = []
    for min, avg, max in start_date_query:
        start_date_dict = {}
        start_date_dict["Minimum Temperature"] = min
        start_date_dict["Average Temperature"] = avg
        start_date_dict["Maximum Temperature"] = max
        start_date_list.append(start_date_dict)

    return jsonify(start_date_list)


########## Start / End Route ##########

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create session from Python to the DB
    session = Session(engine)

    # Query Start End Date
    start_end_date_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    # Convert the query results to a dictionary
    start_end_date_list = []
    for min, avg, max in start_end_date_query:
        start_end_date_dict = {}
        start_end_date_dict["Minimum Temperature"] = min
        start_end_date_dict["Average Temperature"] = avg
        start_end_date_dict["Maximum Temperature"] = max
        start_end_date_list.append(start_end_date_dict)

    return jsonify(start_end_date_list)


if __name__ == '__main__':
    app.run(debug=True)