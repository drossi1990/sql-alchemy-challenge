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

#function to calculate previous year dates for a given range
def precipitation(year,month,day):
    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(year, month, day) - dt.timedelta(days=365)
    return(prev_year)
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
        f"/api/v1.0/temp/start+end<br/>"
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
    station_query = session.query(stations.station).all()

    # Unravel results into a 1D array and convert to a list
    station_list = list(np.ravel(station_query))
    return jsonify(stations=stations)


# @app.route('/api/v1.0/tobs')
# @app.route('/api/v1.0/temp/<start>')
# @app.route('/api/v1.0/temp/<start>/<end>')

if __name__ == '__main__':
    app.run()