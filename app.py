# Import the dependencies.
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from dateutil.relativedelta import relativedelta
import pandas as pd
#pip install python-dateutil

#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station_data = Base.classes.station
measurement_data = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
def app_func_precipitation():
    recent_date = session.query(func.max(measurement_data.date)).first()
    start_date = (dt.datetime.strptime(recent_date[0], '%Y-%m-%d') - dt.timedelta(days=365)).date()
    query = session.query(measurement_data.date, measurement_data.prcp).filter(measurement_data.date >= start_date).all()
    session.close()
    output = [dict(query)]
    return output

def app_func_stations():
    stations = session.query(station_data).all()
    session.close()
    stations_list = []

    for station in stations:
        station_dictionary = {}
        station_dictionary[station.station] = {
            'name': station.name,
            'lat': station.latitude,
            'lng': station.longitude,
            'elevation': station.elevation
        }
        stations_list.append(station_dictionary)

def app_func_tobs():
    stations_counts = session.query(measurement_data.station, func.count(measurement_data.station)). \
        group_by(measurement_data.station). \
        order_by(func.count(measurement_data.station).desc()).all()
    stations_counts
    station = stations_counts[0][0]
    df = pd.DataFrame(session.query(measurement_data.tobs, measurement_data.date, measurement_data.station))
    df = df[df['station'] == station]
    df['date'] = pd.to_datetime(df['date'])
    df_delta = df[df['date'] >= df['date'].max() - relativedelta(days=364)]
    return df_delta

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return '''
        <head>
            <title>Hawai temperature API</title>
            <style>
                .style_site {
                    background-color: powderblue;
                    font-family: verdana;
                    border-radius: 7px;}
            </style>
        </head>
        <body>
            <h1>The bootcamp GWU Wheater API assignment</h1>
            <hr/>
            <hr/>
            <ul>
                <li>Precipitation analysis (<a href='../precipitation'>click here</a>)</li>
                <li>For the stations (<a href='../stations'>click here</a>)</li>
                <li>Temperatures of the most-active station(<a href='../tobs'>click here</a>)</li>
                <li>               
                    <b>Insert information in boxes below to get date range data</b><br/>
                    <form>
                        <label>Start Date</label>&ensp;<input type='text' id='start'><br/>
                        <label>End Date</label>&ensp;&nbsp;<input type='text' id='end'><br/>
                        <input type='button' value='Submit' onclick="goto(document.getElementById('start'), document.getElementById('end'))">
                    </form>
                </li>
            </ul>
            <script>
                function goto(start, end) {
                    if ((start && start.value) && (end && end.value)) {window.location.href='../' + start.value + '/' + end.value;}
                     else if ((start && start.value) && !(end && end.value)) {window.location.href='../' + start.value;}
                     else {window.location.href='../error';}
                }
            </script>
'''

@app.route('/precipitation')
def get_precipitation():
    output = app_func_precipitation()
    return jsonify(output)

@app.route('/stations')
def get_stations():
    output = app_func_stations()
    return jsonify(output)

@app.route('/tobs')
def get_tobs():
    output = app_func_tobs()
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)


