# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,desc

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base =automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)
Base.classes.keys

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Helper Function
#################################################
def get_one_year_before_date():
    """Get the date one year before the most recent date in the dataset."""
    session = Session(engine)

    most_recent_date = session.query(measurement.date).order_by(desc(measurement.date)).first()
    session.close()

    most_recent_date_string = most_recent_date[0]
    most_recent_date_obj = dt.datetime.strptime(most_recent_date_string, '%Y-%m-%d').date()
    one_year_before_date = most_recent_date_obj - dt.timedelta(days=365)

    return one_year_before_date

def tempertaure_data(start, end=None):
    """Get the min, avg, and max temperatures for a given date range."""
    session = Session(engine)

    tobs = [
        func.min(measurement.tobs),
        func.max(measurement.tobs),
        func.avg(measurement.tobs)]
    
    if end:
        temperatures = session.query(*tobs).filter(measurement.date >= start, measurement.date <= end).all()
    else:
        temperatures = session.query(*tobs).filter(measurement.date >= start).all()
    
    session.close()

    return list(temperatures[0])


def temperature_response(temperature_list):
    """Format the temperature data as a JSON response."""
    return jsonify({
        "TMIN": temperature_list[0],
        "TMAX": temperature_list[1],
        "TAVG": temperature_list[2]
    })




#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the query results from the precipitation analysis in JSON"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Get the date one year before
    one_year_before_date = get_one_year_before_date()
    
    #Query the precipitation data for the most recent 12 months    
    precipitation_data= session.query(measurement.prcp,measurement.date).\
    filter(measurement.date >= one_year_before_date).all()

    #Close the session
    session.close()

    precipitation ={}
    for prcp,date in precipitation_data:
        precipitation[date] = prcp

    return jsonify (precipitation)   

@app.route("/api/v1.0/stations") 
def stations ():
    """Return a JSON list of stations from the dataset """

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query the station from the dataset
    stations= session.query(measurement.station).group_by(measurement.station).all()

    #Close the session
    session.close()

    #Conversion of the above list of tuples into a flat list
    station_list = [station[0] for station in stations]

    # Return the list as a JSON response
    return jsonify(station_list)
    
@app.route("/api/v1.0/tobs")
def active_station_temp():
     """Return a JSON list of temperature observations of most active station for the previous year """

      # Create our session (link) from Python to the DB
     session = Session(engine)

      # Get the date one year before
     one_year_before_date = get_one_year_before_date()
    
     #finding the most ative station
     active_station = session.query(measurement.station).\
     group_by(measurement.station).\
     order_by(desc(func.count(measurement.station))).first()

     #Query the dates and temperature observations for that station for last year
     temp = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= one_year_before_date).\
        filter(measurement.station==active_station[0]).all()
     
     #Close the session
     session.close()

     #Conversion of the above list of tuples into a flat list
     temp_date_list = [data[1] for data in temp]

    # Return the list as a JSON response
     return jsonify(temp_date_list)

@app.route("/api/v1.0/<start>")  
def start_date(start):
     """Return a JSON list of the min temperature, the avg temperature, 
    and the max temperature for the date supplied by the user"""

     # Create our session (link) from Python to the DB
     session = Session(engine)
     
    #Get average,minimum and maximum temperature values for the start date and above accpeted as a URL parameter
     temperature_list = tempertaure_data(start)

     #Close the session
     session.close()

     # Return the list as a JSON response
     return temperature_response(temperature_list)

@app.route("/api/v1.0/<start>/<end>")  
def start_end_date(start,end):
     """Return a JSON list of the min temperature, the avg temperature, 
    and the max temperature within the date ranges supplied by the user"""

     # Create our session (link) from Python to the DB
     session = Session(engine)
     
    #Get average,minimum and maximum temperature values for the date ranges accpeted as a URL parameter
     temp_list = tempertaure_data(start,end)
     #Close the session
     session.close()

     # Return the list as a JSON response
     return temperature_response(temp_list)

if __name__ == '__main__':
    app.run(debug=True)        