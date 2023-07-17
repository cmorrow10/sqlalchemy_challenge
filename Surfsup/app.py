# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# 1. /
# Start at the Home page
# List all available routes
@app.route("/")
def homepage():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate<br/>"
        f"/api/v1.0/startdate/enddate"
    )

# 2. /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using "date" as the key and "prcp" as the value
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Return the JSON representation of your dictionary
    all_date = []
    for date, prcp in results:
        date_prcp_dict = {}
        date_prcp_dict["date"] = date
        date_prcp_dict["prcp"] = prcp
        all_date.append(date_prcp_dict)
    
    return jsonify(all_date)

# 3. /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    results = session.query(Station.station, Station.name).all()

    session.close()

    # Return a JSON list of stations from the dataset
    all_stations = []
    for station, name in results:
        all_stations_dict = {}
        all_stations_dict["station"] = station
        all_stations_dict["name"] = name
        all_stations.append(all_stations_dict)
    
    return jsonify(station_list)

# 4. /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

# Query the dates and temperature observations of the most-active station for the previous year of data
    last_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = (dt.datetime.strptime(last_day[0], "%Y-%m-%d") - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    
    active_station = session.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()
    
    results = session.query(Measurement.tobs).filter(Measurement.date >= query_date).\
filter(Measurement.station == active_station[0]).all()

    session.close()


# Return a JSON list of temperature observations for the previous year
info_active_station = list(np.ravel(results))

return jsonify(info_active_station)

# 5. /api/v1.0/<start> and /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>")
def start_date(start):

    session = Session(engine)

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range
    results = session.query(Measurement.date,func.min(Measurement.tobs),\
        func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()

    session.close()

# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
    info = []
    for date, min, avg, max in results:
        info_dict = {}
        info_dict["DATE"] = date
        info_dict["TMIN"] = min
        info_dict["TAVG"] = avg
        info_dict["TMAX"] = max
        info.append(info_dict)

    return jsonify(info)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

    session = Session(engine)

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range
    results = session.query(func.min(Measurement.tobs),\
        func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive
    info = []

    for min, avg, max in results:
        info_dict = {}
        info_dict["TMIN"] = min
        info_dict["TAVG"] = avg
        info_dict["TMAX "] = max
        info.append(info_dict)

    return jsonify(info)



if __name__ == "__main__":
    app.run(debug = True)