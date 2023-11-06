# Import the dependencies.
import datetime as dt
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
        return stations_list

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
    df = df_delta.to_json()
    return df

def date_validate(date):
    check_pass = False
    try:
        year, month, day = date.split('-')
        dt.datetime(int(year), int(month), int(day))
        check_pass = True
    except:
        return check_pass
    return check_pass

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
    return output

@app.route('/<start>')
def get_temp_start(start):
    start_date = date_validate(start)
    if start_date:
        query = session.query(func.min(measurement_data.tobs), func.max(measurement_data.tobs),
                              func.avg(measurement_data.tobs)).filter(measurement_data.date >= start).all()
        session.close()
        if not query[0][0] is None:
            result = []
            result.append({
                'min': query[0][0],
                'max': query[0][1],
                'avg': query[0][2]
            })
            return jsonify(result)
        return jsonify({"Date entry error"}), 404
    return jsonify({"Date entry error"}), 404


@app.route('/<start>/<end>')
def get_temp_start_end(start, end):
    start_date = date_validate(start)
    end_date = date_validate(end)
    if start_date and end_date:
        if not start.replace('-', '') > end.replace('-', ''):
            query = session.query(func.min(measurement_data.tobs), func.max(measurement_data.tobs), func.avg(measurement_data.tobs)). \
                filter(measurement_data.date >= start, measurement_data.date <= end).all()
            session.close()
            if not query[0][0] is None:
                result = []
                result.append({
                    'min': query[0][0],
                    'max': query[0][1],
                    'avg': query[0][2]
                })
                return jsonify(result)
            return jsonify({"Date entry error."}), 404
        return jsonify({"Date entry error"}), 404
    return jsonify({"Date entry error"}), 404

if __name__ == "__main__":
    app.run(debug=True)


