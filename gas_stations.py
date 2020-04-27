import requests
import json
import os
import numpy as np
import googlemaps
import math

googlekey = os.environ['PLACES_KEY']
placesAPI = googlemaps.Client(key= googlekey)
data_json_file = open('data/mapsAPI/neighborhood_data.json')
neighborhood_data = json.load(data_json_file)
data_json_file.close()

valid_neighborhood_gas_stations = {}
valid_neighborhood_gas_station_distances = {}
neighborhood_gas_station_scores = {}

for neighborhood_name in neighborhood_data.keys():
    file_directory_template = 'data/mapsAPI/'
    infile = open(file_directory_template + neighborhood_name + '_gas_stations.json')
    curr_gas_stations_dict = json.load(infile)
    infile.close()
    temp_valid_gas_stations = []
    for i in range(20):
        curr_gas_station_id = curr_gas_stations_dict['results'][i]['place_id']
        curr_place = placesAPI.place(
                        place_id=curr_gas_station_id,
                        language='EN',
                        fields=['place_id',
                                'address_component',
                                'permanently_closed',
                                'type',
                                'geometry/location/lat',
                                'geometry/location/lng'])
        for i in range(len(curr_place['result']['address_components'])):
            if curr_place['result']['address_components'][-i]['types'] == ['postal_code']:
                if int(curr_place['result']['address_components'][-i]['short_name']) < 10300 and \
                 int(curr_place['result']['address_components'][-i]['short_name']) > 9999:
                    temp_valid_gas_stations.append(curr_place)
                    break
            if curr_place['result']['address_components'][-i]['types'] == ['postal_code']:
                if int(curr_place['result']['address_components'][-i]['short_name']) >= 10300 or \
                 int(curr_place['result']['address_components'][-i]['short_name']) <= 9999:
                    break
    fully_valid_gas_stations = []
    fully_valid_gas_station_distances = []
    # max valid distance of gas station from neighborhood center
    max_distance = 1.5
    lat_neighborhood_center = math.radians(neighborhood_data[neighborhood_name]['center'][0])
    lng_neighborhood_center = math.radians(neighborhood_data[neighborhood_name]['center'][1])
    for gas_station in temp_valid_gas_stations:
        gas_station_coordinates = [gas_station['result']['geometry']['location']['lat'],
                                   gas_station['result']['geometry']['location']['lng']]
        lat_gas_station = math.radians(gas_station_coordinates[0])
        lng_gas_station = math.radians(gas_station_coordinates[1])
        lat_diff = lat_gas_station - lat_neighborhood_center
        lng_diff = lng_gas_station - lng_neighborhood_center
#         haversine formula for calculating distance, from https://kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python
        temp_a = np.square(math.sin(lat_diff / 2)) + \
                 math.cos(lat_neighborhood_center) * math.cos(lat_gas_station) * np.square(math.sin(lng_diff / 2))
        temp_c = 2 * math.atan2(math.sqrt(temp_a), math.sqrt(1 - temp_a))
        # distance is in miles
        distance = temp_c * 3959
        if distance < max_distance:
            fully_valid_gas_stations.append(gas_station)
            fully_valid_gas_station_distances.append(distance)
    fully_valid_gas_station_distances = np.asarray(fully_valid_gas_station_distances)
    valid_neighborhood_gas_stations[neighborhood_name] = fully_valid_gas_stations
    valid_neighborhood_gas_station_distances[neighborhood_name] = fully_valid_gas_station_distances
    neighborhood_gas_station_scores[neighborhood_name] = \
        np.nan_to_num(np.sum(max_distance - fully_valid_gas_station_distances))

    print(neighborhood_name, len(valid_neighborhood_gas_stations[neighborhood_name]),
                                 neighborhood_gas_station_scores[neighborhood_name])