import csv
from flask import Flask, jsonify
from model import Region, Station_name, dbconnect

app = Flask(__name__)

@app.route('/region/<search_term>', methods=['GET'])
def get_region(search_term):
	session = dbconnect()
	try:
	    region_instance = session.query(Region).filter(Region.region == search_term).one()
	    return jsonify(region_instance.id), 200
	except:
		return "Region doesn't exist in database", 400

if __name__ == '__main__':
    app.run(debug=True)