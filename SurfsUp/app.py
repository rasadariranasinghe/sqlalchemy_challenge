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
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def Home():
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
def Precipitation():
    """Return the query results from the precipitation analysis in JSON"""

    #Query the precipitation data for the most recent 12 months

    most_recent_date= session.query(Measurement.date).order_by(desc(Measurement.date)).first()

    most_recent_date_string = most_recent_date[0]
    most_recent_date_obj = dt.datetime.strptime(most_recent_date_string, '%Y-%m-%d').date()
    one_year_before_date = most_recent_date_obj - dt.timedelta(days=365)
    
    precipitation_data= session.query(Measurement.prcp,Measurement.date).\
    filter(Measurement.date >= one_year_before_date).all()

    session.close()
    precipitation ={}
    for prcp,date in precipitation_data:
        precipitation[date] = prcp

    return jsonify (precipitation)   

@app.route("/api/v1.0/stations") 
def Stations ():

    """Return a JSON list of stations from the dataset """

    #Query the station from the dataset

    stations= session.query(Measurement.station).group_by(Measurement.station).all()

    #Conversion of the above list of tuples into a flat list
    station_list = [station[0] for station in stations]
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def Active_station_temp():

     """Return a JSON list of temperature observations of most active station for the previous year """

     most_recent_date= session.query(Measurement.date).order_by(desc(Measurement.date)).first()

     most_recent_date_string = most_recent_date[0]
     most_recent_date_obj = dt.datetime.strptime(most_recent_date_string, '%Y-%m-%d').date()
     one_year_before_date = most_recent_date_obj - dt.timedelta(days=365)
    
     #finding the most ative station
     active_station = session.query(Measurement.station).\
     group_by(Measurement.station).\
     order_by(desc(func.count(Measurement.station))).first()

     #Query the dates and temperature observations for that station for last year
     temp = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_before_date).\
        filter(Measurement.station==active_station[0]).all()
     
     temp_date_list = [data[1] for data in temp ]
     return jsonify(temp_date_list)

@app.route("/api/v1.0/<start>")  
def Start_date(start):
     """Return a JSON list of the min temperature, the avg temperature, 
    and the max temperature supplied by the user"""

     
     temperatures = session.query(
     func.min(Measurement.tobs),
     func.max(Measurement.tobs),
     func.avg(Measurement.tobs)).\
        filter(Measurement.date  >= start ).all()

     temperature_list = list(temperatures[0])
     return (temperature_list)
      

@app.route("/api/v1.0/<start>/<end>")  
def Start_end_date(start,end):


     temperatures = session.query(
     func.min(Measurement.tobs),
     func.max(Measurement.tobs),
     func.avg(Measurement.tobs)).\
        filter (Measurement.date >= start, Measurement.date<= end).all()

     temp_list = list(temperatures[0])
     return (temp_list)

if __name__ == '__main__':
    app.run(debug=True)        