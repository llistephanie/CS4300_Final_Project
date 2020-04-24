# https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY

import requests
import json
import csv
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", 
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5", 
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1", 
    "Connection": "close", 
    "Upgrade-Insecure-Requests": "1",
    "Origin": "http://niche.com/",
    "Access-Control-Request-Method": "GET",
    "Access-Control-Request-Headers": "X-Requested-With" }

YOUR_API_KEY="AIzaSyDkJTfA9iboEc6Wc1y-FEPrH3-wIBfonDE"

data={}

with open('data/neighborhoods.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count+=1
            continue
        neighborhood_data={}
        google_name=row[1].replace(' ', '+')
        response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={google_name},+NY&key={YOUR_API_KEY}", headers=headers)
        # print(list(response.json()['results'][0].keys()))
        neighborhood_data['geometry']=response.json()['results'][0]['geometry']
        neighborhood_data['place_id']=response.json()['results'][0]['place_id']
        data[row[1]]=neighborhood_data

with open("coordinates.txt", 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address=Battery+Park+City,+NY&key={YOUR_API_KEY}", headers=headers)

# print(response.json()['address_components']['geometry'])
# #         soup = BeautifulSoup(response.text, "html.parser")
#         results = soup.find(id='app')

# https://github.com/HodgesWardElliott/custom-nyc-neighborhoods