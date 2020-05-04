import numpy as np
import googlemaps
import os
import json
import shapely
import pyproj
from shapely import geometry
from shapely.ops import transform

googlekey = os.environ['PLACES_KEY']
placesAPI = googlemaps.Client(key= googlekey)
file_directory_template = 'app/irsystem/controllers/data/'
with open(file_directory_template + 'exact-bounds.json', 'r') as infile:
    exact_bounds = json.load(infile)
neighborhood_polygons = {}
for neighborhood_name, neighborhood_bounds in exact_bounds.items():
    curr_neighborhood_boundaries = neighborhood_bounds['geometry']['coordinates']
    assert len(curr_neighborhood_boundaries) == 1
    neighborhood_polygons[neighborhood_name] = geometry.Polygon(curr_neighborhood_boundaries[0])

# deal with central park separately
# sources: https://www.timeout.com/newyork/attractions/new-york-attractions
# https://trending.virginholidays.co.uk/new-york-city/attractions
# Google Maps
attractions = ['Empire State Building',
               'Times Square',
               'Brooklyn Bridge',
               'Rockefeller Center',
               'Statue of Liberty',
               'Hudson Yards',
               'One World Trade Center',
               'Metropolitan Museum of Art',
               'The High Line',
               'New York Stock Exchange',
               'Grand Central Terminal',
               'Madison Square Garden',
               'New York Public Library',
               'New-York Historical Society',
               'Guggenheim Museum',
               'Chelsea Market',
               'Apollo Theater',
               'Yankee Stadium',
               'American Museum of Natural History',
               'Union Square',
               'United Nations',
               'Chrysler Building',
               'New York City Hall',
               'Flatiron Building',
               'The Cloisters',
               'Intrepid Sea, Air and Space Museum',
               'Lincoln Center',
               'Museum of Modern Art (MoMA)',
               'Radio City Music Hall',
               "St Patrick's Cathedral",
               'Bryant Park',
               'Brooklyn Battery Park',
               'Gramercy Park',
               'Cornell Tech',
               'Whitney Museum of American Art',
               'Museum of the City of New York',
               'Brookfield Place',
               'National Museum of the Amerian Indian',
               'Manhattan Bridge',
               'Williamsburg Bridge',
               'Fort Washington Park',
               'George Washington Bridge',
               "Grant's Tomb",
               '9/11 Memorial',
               'Columbia University',
               'New York University',
               'Morningside Park',
               "Macy's Herald Square",
               'Fort Tryon Park',
               'Edgar Allen Poe Cottage',
               'Inwood Hill Park',
               'Museum of Chinese in America',
               'International Center of Photography Museum',
               'Washington Square Park',
               'National Arts Club',
               'New Museum',]

central_park_attraction = placesAPI.find_place(input="Central Park",
                                               input_type="textquery",
                                               fields=['name', 'formatted_address', 'geometry'],
                                               location_bias='rectangle:40.699173,-74.022022|40.878975,-73.898665')['candidates'][0]

query_google = input("Query Google Places for updated attraction_results? y/[n]")
if query_google == "y" or query_google == "yes":
    attraction_results = {}
    for attraction_name in attractions:
        curr_attraction_results = placesAPI.find_place(input=attraction_name,
                                                       input_type="textquery",
                                                       fields=['name', 'formatted_address', 'geometry'],
                                                       location_bias='rectangle:40.699173,-74.022022|40.878975,-73.898665')
        attraction_results[attraction_name] = curr_attraction_results['candidates'][0]
        print(attraction_name, curr_attraction_results['candidates'][0])
    with open(file_directory_template + 'attractions.json', 'w') as outfile:
        json.dump(attraction_results, outfile)
else:
    with open(file_directory_template + 'attractions.json', 'r') as infile:
        attraction_results = json.load(infile)
attraction_points = {}
for attraction_name, attraction in attraction_results.items():
    attraction_points[attraction_name] = geometry.Point(attraction['geometry']['location']['lng'], attraction['geometry']['location']['lat'])
    print(attraction_points[attraction_name])

wgsProjection = pyproj.Proj('epsg:4326')
nadProjection = pyproj.Proj('epsg:2260')
project_to_nad = pyproj.Transformer.from_proj(wgsProjection, nadProjection)
project_to_wgs = pyproj.Transformer.from_proj(nadProjection, wgsProjection)

# cparknadProjection = pyproj.Proj('epsg:2263')
# cpark_project_to_wgs = pyproj.Transformer.from_proj(cparknadProjection, wgsProjection)
with open('data/central_park_shapefile.geoJSON', 'r') as infile:
    temp = json.load(infile)
    print(temp['features'][0])
    central_park_polygon = geometry.Polygon(temp['features'][0]['geometry']['coordinates'][0])
print(central_park_polygon)

neighborhood_buffers_660 = {}
neighborhood_buffers_1320 = {}
neighborhood_attractions = {}
for neighborhood_name, currpolygon in neighborhood_polygons.items():
    neighborhood_attractions[neighborhood_name] = []
    temp_1320 = transform(project_to_nad.transform, currpolygon).buffer(1320)
    currbuffer_1320 = transform(project_to_wgs.transform, temp_1320)
    neighborhood_buffers_1320[neighborhood_name] = currbuffer_1320
    temp_660 = transform(project_to_nad.transform, currpolygon).buffer(660)
    currbuffer_660 = transform(project_to_wgs.transform, temp_660)
    neighborhood_buffers_660[neighborhood_name] = currbuffer_660
    # checking if neighborhood is near Central Park; if so, adds Central Park to attractions list
    if neighborhood_buffers_660[neighborhood_name].intersects(central_park_polygon):
        neighborhood_attractions[neighborhood_name].append(central_park_attraction)
    # only the buffer up to 660ft away (excluding original polygon)
    currbuffer_660_diff = currbuffer_660.difference(currpolygon)
    # just the buffer btw 660ft and 1/4 mile away
    currbuffer_1320_diff = currbuffer_1320.difference(currbuffer_660)
    # first adds results within the neighborhood, followed by closer attractions and finally the furthest attractions
    for attraction_name, currpoint in attraction_points.items():
        if currpolygon.contains(currpoint):
            neighborhood_attractions[neighborhood_name].append(attraction_results[attraction_name])
    for attraction_name, currpoint in attraction_points.items():
        if currbuffer_660_diff.contains(currpoint):
            neighborhood_attractions[neighborhood_name].append(attraction_results[attraction_name])
    for attraction_name, currpoint in attraction_points.items():
        if currbuffer_1320_diff.contains(currpoint):
            neighborhood_attractions[neighborhood_name].append(attraction_results[attraction_name])
    neighborhood_attractions[neighborhood_name] = neighborhood_attractions[neighborhood_name][:3]
    print(neighborhood_name, [attraction['name'] for attraction in neighborhood_attractions[neighborhood_name]])

with open(file_directory_template + 'neighborhood-attractions.json', 'w') as outfile:
    json.dump(neighborhood_attractions, outfile)