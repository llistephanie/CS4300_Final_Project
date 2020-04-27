import requests
import json
import os
import numpy as np
import googlemaps

googlekey = os.environ['PLACES_KEY']
coordinate_json_file = open('app/irsystem/controllers/data/coordinates.json')
neighborhood_json = json.load(coordinate_json_file)
coordinate_json_file.close()
neighborhood_data = {}
neighborhood_names = []

for neighborhood_name in neighborhood_json.keys():
    neighborhood_names.append(neighborhood_names)
    NE_lat = neighborhood_json[neighborhood_name]['geometry']['viewport']['northeast']['lat']
    NE_lng = neighborhood_json[neighborhood_name]['geometry']['viewport']['northeast']['lng']
    SW_lat = neighborhood_json[neighborhood_name]['geometry']['viewport']['southwest']['lat']
    SW_lng = neighborhood_json[neighborhood_name]['geometry']['viewport']['southwest']['lng']
    curr_area = np.abs(NE_lat - SW_lat) * np.abs(NE_lng - SW_lng)
    neighborhood_dict = {}
    neighborhood_dict['northeast'] = [NE_lat, NE_lng]
    neighborhood_dict['southwest'] = [SW_lat, SW_lng]
    neighborhood_dict['area'] = curr_area
    neighborhood_dict['center'] = [neighborhood_json[neighborhood_name]['geometry']['location']['lat'],
                                   neighborhood_json[neighborhood_name]['geometry']['location']['lng']]
    neighborhood_data[neighborhood_name] = neighborhood_dict

gas_stations = {}
for neighborhood_name in neighborhood_data.keys():
    curr_gas_stations_dict = placesAPI.places_nearby(keyword='gas station',
                                                     rank_by='distance',
                                                     location=str(neighborhood_data[neighborhood_name]['center'][0]) + \
                                                     ", " + str(neighborhood_data[neighborhood_name]['center'][1]),
                                                     type='gas_station',
                                                     language='EN')
    file_directory_template = 'data/mapsAPI/'
    with open(file_directory_template + neighborhood_name + '_gas_stations.json', 'w') as outfile:
        json.dump(curr_gas_stations_dict, outfile)

with open(file_directory_template + 'neighborhood_data.json', 'w') as outfile:
        json.dump(neighborhood_data, outfile)