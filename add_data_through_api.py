import csv
import requests
# This is very broken but should provide you with excellent clues on how to proceed.

def wrangle(input_dict):
    # Try and get the station ID with a GET
	region_request = requests.get("http://127.0.0.1:5000/region/{}".format(input_dict["Region"]))
    # If the get returns 400 (http status code for "not found"). then try to add it with a POST.
	if region_request.status_code == 400:
		region_request = requests.post("http://127.0.0.1:5000/region" , json=pload_region)
    # Add the returned region id to the dictionary so we can add a station.
	input_dict["region_id"] = region_request.text 
	requests.post("http://127.0.0.1:5000/station" , json=input_dict)



with open(r"short_train_station_data_uk.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for station_name in reader:
        wrangle(station_name)