import csv
from flask import Flask, jsonify, request
from model import Region, Station, dbconnect
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

#Readme: https://www.w3schools.com/tags/ref_httpmethods.asp


@app.route('/region/<search_term>', methods=['GET'])
def get_region(search_term):
    session = dbconnect()
    try:
        region_instance = session.query(Region).filter(Region.region == search_term).one()
        return jsonify(region_instance.id), 200
    except:
        # print(e)
        return "Region doesn't exist in database", 400

@app.route('/station/<search_term>', methods=['GET'])
def get_station(search_term):
    session = dbconnect()
    try:
        station_instance = session.query(Station).filter(Station.station_name == search_term).one()
        return jsonify(station_instance.id), 200
    except:
        # print(e)
        return "Station doesn't exist in database", 400

# What the hell does this post endpoint do!!
@app.route('/region', methods=['POST'])
def add_region():
    session = dbconnect()
    request_dict = request.get_json()
    try: # Try to create the region
        region_instance = Region()
        region_instance.region = request_dict["Region"]
        session.add(region_instance)
        session.commit()
        return jsonify(region_instance.id)
    except exc.IntegrityError: # If the region doesn't exist - freak out and send back 400.
        session.rollback()
        return "already exists", 400

# What the hell does this post endpoint do!!
@app.route('/station', methods=['POST'])
def add_station():
    session = dbconnect()
    request_dict = request.get_json()
    try: 
        region_instance = session.query(Region).filter(Region.id == request_dict["region_id"]).one()
    except:
        return "Region ID doesn't exist in database", 400

    
    try: # Try to create the station
        station_instance = Station()
        station_instance.station_name = request_dict["Station Name"]
        station_instance.NLC = request_dict["NLC"]
        station_instance.TLC = request_dict["TLC"]
        station_instance.local_authority = request_dict["Local Authority"]
        station_instance.constituency = request_dict["Constituency"]
        station_instance.NUTS2_spatial_unit = request_dict["NUTS2 Spatial Unit"]
        station_instance.NUTS2_spatial_unit_code = request_dict["NUTS2 Spatial_Unit Code"]
        station_instance.OS_grid_easting = request_dict["OS Grid Easting"]
        station_instance.OS_grid_northing = request_dict["OS Grid Northing"]
        station_instance.Station_Facility_Owner = request_dict["Station Facility Owner"]
        station_instance.Network_Rail_Region_of_station = request_dict["Network Rail Region of station"]
        station_instance.Entries_Exits_Full = request_dict["Entries Exits_Full"]
        station_instance.Entries_Exits_Reduced = request_dict["Entries Exits_Reduced"]
        station_instance.Entries_Exits_Season= request_dict["Entries Exits_Season"]
        station_instance.A1819_Entries_Exits = request_dict["A1819 Entries Exits"]
        station_instance.B1718_Entries_Exits = request_dict["B1718 Entries Exits"]
        station_instance.C1819_Interchanges = request_dict["C1819 Interchanges"]
        station_instance.D1819_Entries_Exits_GB_Rank = request_dict["D1819 Entries Exits GB rank"]
        station_instance.E1718_Entries_Exits_GB_Rank = request_dict["E1718 Entries Exits GB rank"]
        station_instance.Change = request_dict["Change"]
        station_instance.region = region_instance
        session.add(station_instance)
        session.commit()
        return jsonify(station_instance.id)
    except exc.IntegrityError: # If the station doesn't exist - freak out and send back 400.
        session.rollback()
        return "already exists", 400
    

if __name__ == '__main__':
    app.run(debug=True)