import requests
import json
import os
import numpy as np
import googlemaps
import math
import shapely

neighborhood_outlines = {}
neighborhood_outlines_query = "https://data.opendatasoft.com/api/records/1.0/search/" +\
                                       "?dataset=zillow-neighborhoods%40public&facet=state&facet=county" + \
                                       "&facet=city&facet=name&refine.state=NY&refine.county=New+York"
neighborhood_outlines_response = requests.get(neighborhood_outlines_query)
neighborhood_outlines_json_records = json.loads(neighborhood_outlines_response.text)["records"]
for neighborhoodindex, neighborhood_json in enumerate(neighborhood_outlines_json_records):
    neighborhood_name = neighborhood_json['fields']['name']
    neighborhood_outlines[neighborhood_name] = neighborhood_json['fields']['geo_shape']['coordinates']
    print(neighborhood_outlines[neighborhood_name])
    print(neighborhood_name)
print(len(neighborhood_outlines))
print(neighborhood_outlines_query)

neighborhood_data_json_file = open('data/mapsAPI/neighborhood_data.json')
neighborhood_data = json.load(neighborhood_data_json_file)
neighborhood_data_json_file.close()
subway_data_json_file = open("data/Subway Stations.geojson")
subway_data_json = json.load(subway_data_json_file)
subway_data_json_file.close()