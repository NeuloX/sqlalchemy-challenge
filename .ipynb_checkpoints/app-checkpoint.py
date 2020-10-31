import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# HOME
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"-------------------------<br/>"
        f"Get temperature data from the date provided as yyyy-mm-dd <br/>"
         f"-------------------------<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
         f"-------------------------<br/>"
        f"Get temperature data from the date provided as yyyy-mm-dd to 2nd provided date.<br/>"
         f"-------------------------<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

# Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    latest_date = dt.date(2017, 8, 23)
    last_year = dt.timedelta(days=365)
    latest_year = latest_date - last_year
    measure_data = [Measurement.id, Measurement.date, Measurement.prcp, Measurement.station]
    get_data = session.query(*measure_data).filter(Measurement.date >= latest_year).all()
    session.close()

    return jsonify(get_data)

# Stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_data = [Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    get_data = session.query(*station_data).all()
    session.close()
    
    return jsonify(get_data)

# Tobs
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.station == "USC00519281").all()
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.station == "USC00519281").all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.station == "USC00519281").all()
    result = f"The Max Temperature {max_temp}, Min Temperature {min_temp}, Avg Temperature {avg_temp} of USC00519281 WAIHEE 837.5, HI US."
    session.close()

    return(result)

# Start
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    measure_data = [Measurement.id, Measurement.date, Measurement.prcp, Measurement.station]
    tmax = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    tmin = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).all()
    tavg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    result = f"The Max Temperature {tmax}, Min Temperature {tmin}, Avg Temperature {tavg} from the date {start} to 2017, 8, 23."
    session.close()
    
    return jsonify(result)
# Start to END
@app.route("/api/v1.0/<start>/<end>")
def start_to_end(start,end):
    session = Session(engine)
    measure_data = [Measurement.id, Measurement.date, Measurement.prcp, Measurement.station]
    tmax = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    tmin = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    tavg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    result = f"The Max Temperature {tmax}, Min Temperature {tmin}, Avg Temperature {tavg} from the date {start} to {end}."
    session.close()
    
    return jsonify(result)

# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)