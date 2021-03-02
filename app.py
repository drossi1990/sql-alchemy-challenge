import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#----------------
# Database Setup
#----------------
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#reflect database and tables into model
Base = automap_base()
Base.prepare(engine, reflect=True)
measurements = Base.classes.measurement
stations = Base.classes.station

#instantiate session from Python to DB
this_session = Session(engine)

app = Flask(__name__)
@app.route('/')
def landing_page():
    return (
        f"------------------------------------------------------------------<br/>"
        f"Hawaii Weather Database API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start_end<br/>"
        f"TEMP Instructions, append Yr(xxxx)-Mo(xx)-Day(xx) to /api/v1.0/temp/ to see past weather for your trip dates!"
        f"------------------------------------------------------------------<br/>"
        f'"Just Another Day in Paradise!"<br/>'
        #Palm Tree ASCII art just for fun
        f"###########################'*`################################<br/>"
        f"###########################***V##'############################<br/>"
        f"#########################V'**`V***############################<br/>"
        f"########################V'*******,############################<br/>"
        f"#########`#############V********,A###########################V<br/>"
        f"########'*`###########V*******,###########################V',#<br/>"
        f"######V'***###########l*******,####################V~~~~'',###<br/>"
        f"#####V'****###########l******##P'*###########V~~'***,A#######<br/>"
        f"#####l******d#########l******V'**,#######V~'*******A#########<br/>"
        f"#####l******##########l*********,####V''*********,###########<br/>"
        f"#####l********`V######l********,###V'***.....;A##############<br/>"
        f"#####A,********`######A,*****,##V'**,A#######################<br/>"
        f"#######A,******* `######A,****#V'**A########'''''##########''<br/>"
        f"##########,,,*******`####A,***********`#''***********'''**,,,<br/>"
        f"#############A,*******************************,,,*****,######<br/>"
        f"######################oooo,*****************;####,*,#########<br/>"
        f"##################P'*******************A,***;#####V##########<br/>"
        f"#####P'****''''*******,###*************`#,*****`V############<br/>"
        f"##P'****************,d###;**************##,*******`V#########<br/>"
        f"##########A,,***#########A**************)##,****##A,..,ooA###<br/>"
        f"#############A,*Y#########A,************)####,*,#############<br/>"
        f"###############A ############A,********,###### ##############<br/>"
        f"###############################*******,#######V##############<br/>"
        f"###############################******,#######################<br/>"
        f"##############################P****,d########################<br/>"
        f"##############################'****d#########################<br/>"
        f"##############################*****##########################<br/>"
        f"##############################*****##########################<br/>"
        f"#############################P*****##########################<br/>"
        f"#############################'*****##########################<br/>"
        f"############################P******##########################<br/>"
        f"###########################P'*****;##########################<br/>"
        f"###########################'*****,###########################<br/>"
        f"##########################*******############################<br/>"
        f"#########################*******,############################<br/>"
        f"########################********d###########P'******.`Y#########<br/>"
        f"#######################********,############*********.#########<br/>"
        f"######################********,#############*********.#########<br/>"
        f"#####################********,##############b.******,d#########<br/>"
        f"####################********,################################<br/>"
        f"###################*********#################################<br/>"
        f"##################**********#######################P'  `V##P'<br/>"
        f"#######P'****`V#***********###################P'<br/>"
        f"#####P'********************,#################P'<br/>"
        f"###P'**********************d##############P''<br/>"
        f"##P'***********************V##############'<br/>"
        f"#P'*************************`V###########'<br/>"
        f"#'*****************************`V##P'<br/>"
    )

#Precipitation Module
@app.route('/api/v1.0/precipitation')
def Precipitation():
    #calculate date 1 year before last date in the db
    last = engine.execute('SELECT max(date) FROM measurement').fetchone()
    Precipitation_1ya = ((dt.datetime.strptime(last[0], '%Y-%m-%d')) - dt.timedelta(days=365))
    Precipitation_Data = this_session.query(measurements.date, measurements.prcp).filter(measurements.date >= Precipitation_1ya).order_by(measurements.date).all()
    Precipitation_Output = {date: prcp for date, prcp in Precipitation_Data}
    return jsonify(Precipitation_Output)

#Station Module
@app.route('/api/v1.0/stations')
def Weather_Stations():
    station_query = this_session.query(stations.station, stations.name).all()

    # Converts query results into a list which can display on the page
    station_list = []
    for s in station_query:
        query_dict = {}
        query_dict['station'] = s.station
        query_dict['name'] = s.name
        station_list.append(query_dict)
    return jsonify(station_list)


@app.route('/api/v1.0/tobs')
def tobs():
   
    last = engine.execute('SELECT max(date) FROM measurement').fetchone()
    tobs_1ya = ((dt.datetime.strptime(last[0], '%Y-%m-%d')) - dt.timedelta(days=365))
    tobs_query = this_session.query(measurements.date, measurements.tobs).filter(measurements.date >= tobs_1ya).all()
    # Converts query results into a list which can display on the page
    tobs_list = []
    for t in tobs_query:
        tobs_dict = {}
        tobs_dict['tobs'] = t.tobs
        tobs_dict['date'] = t.date
        tobs_list.append(tobs_dict)
        
    return jsonify(tobs_list)

@app.route('/api/v1.0/temp/<start>')
def startdate_weather(start):
    #takes startdate as input and returns min, max, and avg temps from startdate to end of record
     startdate = (dt.datetime.strptime(start, '%Y-%m-%d') - dt.timedelta(days=365))
     last = engine.execute('SELECT max(date) FROM measurement').fetchone()
     enddate = dt.datetime.strptime(last[0], '%Y-%m-%d')
     trip_data = this_session.query(func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)).\
                                filter(measurements.date >= startdate).filter(measurements.date <= enddate).all()
     labels = ["min", "max", "avg"]
     temp_stats = {labels[i]: trip_data[0][i] for i in range(len(labels))} 

     return jsonify(temp_stats)


@app.route('/api/v1.0/temp/<start>/<end>')
def startdate_enddate_weather(start,end):
    #takes startdate as input and returns min, max, and avg temps from startdate to enddate
     startdate = (dt.datetime.strptime(start, '%Y-%m-%d') - dt.timedelta(days=365))
     enddate = (dt.datetime.strptime(end, '%Y-%m-%d') - dt.timedelta(days=365))
     trip_data = this_session.query(func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)).\
                                filter(measurements.date >= startdate).filter(measurements.date <= enddate).all()
     labels = ["min", "max", "avg"]
     temp_stats = {labels[i]: trip_data[0][i] for i in range(len(labels))} 

     return jsonify(temp_stats)

if __name__ == '__main__':
    app.run(debug=True)