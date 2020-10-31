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


@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    latest_date = dt.date(2017, 8, 23)
    last_year = dt.timedelta(days=365)
    latest_year = latest_date - last_year
    
    measure_data = [Measurement.id, Measurement.date, Measurement.prcp, Measurement.station]
    get_data = session.query(*measure_data).filter(Measurement.date >= latest_year).all()
    session.close()
    
    precipitation = list(np.ravel(get_data))

    return jsonify(get_data)

@app.route("/api/v1.0/stations")
def stations():
    
    return()

@app.route("/api/v1.0/tobs")
def tobs():
    
    return()

@app.route("/api/v1.0/<start>")
def start():
    
    return()

@app.route("/api/v1.0/<start>/<end>")
def startend():
    
    return()


# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)