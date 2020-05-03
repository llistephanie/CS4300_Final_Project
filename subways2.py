import requests
import json
import os
import numpy as np
import googlemaps
import math
import shapely
import pyproj
from shapely import geometry
from shapely.ops import transform

neighborhood_boundaries = {}
neighborhood_polygons = {}
file_directory_template = 'app/irsystem/controllers/data/'
with open(file_directory_template + 'exact-bounds.json', 'r') as infile:
    exact_bounds = json.load(infile)
for neighborhood_name, neighborhood_bounds in exact_bounds.items():
    neighborhood_boundaries[neighborhood_name] = neighborhood_bounds['geometry']['coordinates']
    assert len(neighborhood_boundaries[neighborhood_name]) == 1
    neighborhood_polygons[neighborhood_name] = geometry.Polygon(neighborhood_boundaries[neighborhood_name][0])

with open("data/Subway Stations.geojson") as infile:
    subway_data_json = json.load(infile)
station_dict = {}
for stationfeature in subway_data_json['features']:
    station_id = stationfeature['properties']['objectid']
    station_name = stationfeature['properties']['name']
    station_lines = stationfeature['properties']['line'].split('-')
    station_coords = stationfeature['geometry']['coordinates']
    station_dict[station_id] = {}
    station_dict[station_id]['name'] = station_name
    station_dict[station_id]['lines'] = station_lines
    station_dict[station_id]['coordinates'] = station_coords

wgsProjection = pyproj.Proj(init='epsg:4326')
# NAD 1983 NY State Plane East
nadProjection = pyproj.Proj(init='epsg:2260')
project_to_nad = pyproj.Transformer.from_proj(wgsProjection, nadProjection)
project_to_wgs = pyproj.Transformer.from_proj(nadProjection, wgsProjection)

neighborhood_buffers = {}
neighborhood_stations = {}
for neighborhood_name, currpolygon in neighborhood_polygons.items():
    temp = transform(project_to_nad.transform, neighborhood_polygons[neighborhood_name]).buffer(2640)
    neighborhood_buffers[neighborhood_name] = transform(project_to_wgs.transform, temp)
    neighborhood_stations[neighborhood_name] = []
    for station_id, station in station_dict.items():
        if neighborhood_buffers[neighborhood_name].contains(geometry.Point(station['coordinates'])):
            neighborhood_stations[neighborhood_name].append(station)

neighborhood_train_raw_scores = []
neighborhood_train_data_dict = {}
for neighborhood_name, nbhd_station_list in neighborhood_stations.items():
    train_list = []
    num_station_services = 0
    num_stations = len(nbhd_station_list)
    for station in nbhd_station_list:
        train_list = train_list + station['lines']
        num_station_services += len(station['lines'])
    train_list = list(set(train_list))
    neighborhood_train_data_dict[neighborhood_name] = {}
    neighborhood_train_data_dict[neighborhood_name]['Station Count'] = num_stations
    # each line in a station adds 1 to its station-service count; for instance, a station with 3 lines adds 3 to any neighborhood containing this station
    neighborhood_train_data_dict[neighborhood_name]['Station-Service Count'] = num_station_services
    neighborhood_train_data_dict[neighborhood_name]['Services'] = train_list
    neighborhood_train_data_dict[neighborhood_name]['Raw Score'] = num_station_services / neighborhood_buffers[neighborhood_name].area
    neighborhood_train_raw_scores.append(neighborhood_train_data_dict[neighborhood_name]['Raw Score'])

max_raw_score = np.amax(np.asarray(neighborhood_train_raw_scores))
for neighborhood_name, nbhd_train_data in neighborhood_train_data_dict.items():
    nbhd_train_data['Score'] = nbhd_train_data['Raw Score'] / max_raw_score * 100
    print(neighborhood_name, nbhd_train_data['Score'])

with open(file_directory_template + 'new_subway_scores.json', 'w') as outfile:
    json.dump(neighborhood_train_data_dict, outfile)