import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv
import json
import os

# headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip, deflate, br", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
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

review_categories = {"Community": "&category=Community&limit=20", "Crime & Safety": "&category=Crime%20%26%20Safety&limit=20",
                     "Overall Experience": "&category=Overall%20Experience&limit=20", "Real Estate": "&category=Real%20Estate&limit=20", "Things To Do": "&category=Things%20To%20Do&limit=20"}

# NICHE CODE
# data = []
# with open('neighborhoods.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             line_count+=1
#             continue
#         elif line_count < 22:
#             line_count+=1
#             continue
#         neighborhood_data={}
#         neighborhood_data["id"]=row[0]
#         neighborhood_data["name"]=row[1]
#         neighborhood_data["niche url"]=row[3]

#         # https://www.niche.com/api/entity-reviews/?e=2bf43857-7ce6-4788-91f1-e497d4d47f7e&category=Crime%20%26%20Safety&limit=20

#         response = requests.get(row[3], headers=headers)
#         soup = BeautifulSoup(response.text, "html.parser")
#         results = soup.find(id='app')
        
#         neighborhood_data["description"]=results.find('span', class_='bare-value').text

#         real_estate_data={}
        
#         real_estate_results = results.find(id='real-estate')
#         real_estate=real_estate_results.find_all('div', class_='scalar')
#         real_estate_data['median home value']=real_estate[0].find_all('div')[1].text.split('National')[0]
#         real_estate_data['median rent']=real_estate[1].find_all('div')[1].text.split('National')[0]
#         real_estate_data['area feel']=real_estate[2].find_all('div')[-1].text.split('National')[0]

#         rent_own=real_estate_results.find_all('div', class_='fact__table__row__value')
#         real_estate_data['rent']=rent_own[0].text
#         real_estate_data['own']=rent_own[1].text

#         neighborhood_data['real estate']=real_estate_data

#         residents_results = results.find(id='residents')
#         residents_data={}
#         residents_data['median household income']=residents_results.find_all('div', class_='scalar__value')[0].text.split('National')[0]
#         residents_data['families with children']=residents_results.find_all('div', class_='scalar__value')[1].text
        
#         neighborhood_data['residents']=residents_data

#         scores={}
#         scores_results=results.find_all('div', class_='profile-grade--two')
#         for i in scores_results:
#             label=i.find_all('div', class_='profile-grade__label')[0].text
#             grade=i.find_all('div', class_='niche__grade')[0].text
#             scores[label]=grade
#         scores["overall_grade"]=results.find('div', class_='niche__grade').text
#         neighborhood_data["scores"]=scores

#         neighborhood_reviews=[]
#         niche_reviews_url="https://www.niche.com/api/entity-reviews/?e="+row[2]

#         for (category, query) in review_categories.items():
#             niche_review_url_cat=niche_reviews_url+query
#             reviews_response = requests.get(niche_review_url_cat, headers=headers)
#             reviews_data=reviews_response.json()
#             try:
#                 for r in reviews_data['reviews']:
#                     review={}
#                     review["stars"]=r['rating']
#                     review["text"]=r['body']
#                     review["category"]=category
#                     neighborhood_reviews.append(review)
#             except KeyError:
#                 pass
                

#         neighborhood_data["reviews"]=neighborhood_reviews
#         with open(row[0]+".txt", 'w', encoding='utf-8') as f:
#             json.dump(neighborhood_data, f, ensure_ascii=False, indent=4)
#         data.append(neighborhood_data)

#         line_count+=1
#     print(f'Processed {line_count} lines.')

# WALK SCORE CODE
walkscore_data = []
with open('neighborhoods.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count+=1
            continue
        
        neighborhood_data={}
        neighborhood_data["id"]=row[0]
        neighborhood_data["name"]=row[1]
        neighborhood_data["walkscore url"]=row[4]

        response = requests.get(row[4], headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        ranking={}
        rankings_data=soup.find('tr', class_='active').find_all('td')
        ranking['rank']=int(rankings_data[0].text)
        ranking['walk score']=int(rankings_data[2].text)
        ranking['transit score']=int(rankings_data[3].text)
        ranking['bike score']=int(rankings_data[4].text)
        ranking['population']=int(rankings_data[5].text.replace(',', ''))
        neighborhood_data['rankings']=ranking

        public_transport={}
        public_transport_data=soup.find('div', class_='transit-route-div').text.replace(',', '').split(' ')
        b="bus"
        s="subway"
        r="rail"
        print(public_transport_data)

        public_transport['bus']=int(public_transport_data[public_transport_data.index(b)-1]) if (b in public_transport_data) else '-'
        public_transport['subway']=int(public_transport_data[public_transport_data.index(s)-1]) if (s in public_transport_data) else '-'
        public_transport['rail']=int(public_transport_data[public_transport_data.index(r)-1]) if (r in public_transport_data) else '-'
        neighborhood_data['public transport']=public_transport

        eating_drinking={}
        # restaurants, bars and coffee shops
        eating_drinking_string=soup.find('div', class_='block-eat-drink').find('div', class_='span12').text
        eating_drinking_data=[int(i) for i in eating_drinking_string.replace(',', '').split() if i.isdigit()] 
        eating_drinking['restaurants']=eating_drinking_data[0]
        eating_drinking['shops']=eating_drinking_data[1]
        eating_drinking['time']=eating_drinking_data[2]

        neighborhood_data['eating drinking']=eating_drinking
        
        walkscore_data.append(neighborhood_data)

        line_count+=1
        
    print(f'Processed {line_count} lines.')

with open("walkscore.txt", 'w', encoding='utf-8') as f:
    json.dump(walkscore_data, f, ensure_ascii=False, indent=4)


# COMBINE JSON
# niche_dir_path='/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/niche'

# # files=os.listdir('/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/niche')
# all_data=[]
# for i in range(0,32):
#     with open(niche_dir_path+'/'+str(i)+'.json') as j:
#         data = json.load(j)
#         all_data.append(data)

# with open("niche.txt", 'w', encoding='utf-8') as f:
#     json.dump(all_data, f, ensure_ascii=False, indent=4)