import requests
import json
import os
import numpy as np
import googlemaps
import math

neighborhood_data_json_file = open('data/mapsAPI/neighborhood_data.json')
neighborhood_data = json.load(neighborhood_data_json_file)
neighborhood_data_json_file.close()
subway_data_json_file = open("data/Subway Stations.geojson")
subway_data_json = json.load(subway_data_json_file)
subway_data_json_file.close()

station_dict = {}
for stationfeature in subway_data_json['features']:
    station_id = stationfeature['properties']['objectid']
    station_name = stationfeature['properties']['name']
    station_lines = stationfeature['properties']['line'].split('-')
    station_coords = [stationfeature['geometry']['coordinates'][1], stationfeature['geometry']['coordinates'][0]]
    station_dict[station_id] = {}
    station_dict[station_id]['name'] = station_name
    station_dict[station_id]['lines'] = station_lines
    station_dict[station_id]['coordinates'] = station_coords
    print(station_lines)

neighborhood_stations = {}
max_distance = 1
neighborhood_raw_scores = {}
for neighborhood_name, neighborhoodobject in neighborhood_data.items():
    lat_neighborhood_center = math.radians(neighborhoodobject['center'][0])
    lng_neighborhood_center = math.radians(neighborhoodobject['center'][1])
    neighborhood_stations = []
    neighborhood_station_distances = []
    neighborhood_station_num_lines = []
    for station_id, stationobject in station_dict.items():
        lat_station = math.radians(stationobject['coordinates'][0])
        lng_station = math.radians(stationobject['coordinates'][1])
        lat_diff = lat_station - lat_neighborhood_center
        lng_diff = lng_station - lng_neighborhood_center
        #         haversine formula for calculating distance, from https://kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python
        temp_a = np.square(math.sin(lat_diff / 2)) + \
                 math.cos(lat_neighborhood_center) * math.cos(lat_station) * np.square(math.sin(lng_diff / 2))
        temp_c = 2 * math.atan2(math.sqrt(temp_a), math.sqrt(1 - temp_a))
        # distance is in miles
        distance = temp_c * 3959
        if distance < max_distance:
            neighborhood_stations.append(stationobject)
            neighborhood_station_distances.append(distance)
            neighborhood_station_num_lines.append(len(stationobject['lines']))
    neighborhood_stations = np.asarray(neighborhood_stations)
    neighborhood_station_distances = np.asarray(neighborhood_station_distances)
    neighborhood_station_num_lines = np.asarray(neighborhood_station_num_lines)
    neighborhood_station_raw_scores = (1 - neighborhood_station_distances) * neighborhood_station_num_lines
    overall_neighborhood_station_raw_score = sum(neighborhood_station_raw_scores)
    neighborhood_raw_scores[neighborhood_name] = overall_neighborhood_station_raw_score

raw_scores = np.array([v for k, v in neighborhood_raw_scores.items()])
max_raw_score = np.amax(raw_scores)
neighborhood_scores = {}
for neighborhood_name, neighborhood_raw_scoresobject in neighborhood_raw_scores.items():
    neighborhood_scores[neighborhood_name] = {}
    neighborhood_scores[neighborhood_name]['score'] = neighborhood_raw_scoresobject / max_raw_score * 100
    print(neighborhood_name, neighborhood_scores[neighborhood_name])

file_directory_template = 'app/irsystem/controllers/data/'
with open(file_directory_template + 'subway_score.json', 'w') as outfile:
    json.dump(neighborhood_scores, outfile)