import csv
from flask import Flask, jsonify, request
from model import Region, Station_name, dbconnect
from sqlalchemy import exc

app = Flask(__name__)

#Readme: https://www.w3schools.com/tags/ref_httpmethods.asp

@app.route('/region/<search_term>', methods=['GET'])
def get_region(search_term):
    session = dbconnect()
    try:
        region_instance = session.query(Region).filter(Region.region_name == search_term).one()
        return jsonify(region_instance.id), 200
    except:
        # print(e)
        return "Region doesn't exist in database", 400

# What the hell does this post endpoint do!!
@app.route('/region', methods=['POST'])
def add_region():
	session = dbconnect()
	request_dict = request.get_json()
	try: # Try to create the region
		region_instance = Region()
		region_instance.region_name = request_dict["Region"]
		session.add(region_instance)
		session.commit()
		return jsonify(region_instance.id)
	except exc.IntegrityError: # If the region doesn't exist - freak out and send back 400.
		session.rollback()
		return "already exists", 400


if __name__ == '__main__':
    app.run(debug=True)