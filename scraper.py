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
# walkscore_data = []
# with open('neighborhoods.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             line_count+=1
#             continue
        
#         neighborhood_data={}
#         neighborhood_data["id"]=row[0]
#         neighborhood_data["name"]=row[1]
#         neighborhood_data["walkscore url"]=row[4]

#         response = requests.get(row[4], headers=headers)
#         soup = BeautifulSoup(response.text, "html.parser")
        
#         ranking={}
#         rankings_data=soup.find('tr', class_='active').find_all('td')
#         ranking['rank']=int(rankings_data[0].text)
#         ranking['walk score']=int(rankings_data[2].text)
#         ranking['transit score']=int(rankings_data[3].text)
#         ranking['bike score']=int(rankings_data[4].text)
#         ranking['population']=int(rankings_data[5].text.replace(',', ''))
#         neighborhood_data['rankings']=ranking

#         public_transport={}
#         public_transport_data=soup.find('div', class_='transit-route-div').text.replace(',', '').split(' ')
#         b="bus"
#         s="subway"
#         r="rail"
#         print(public_transport_data)

#         public_transport['bus']=int(public_transport_data[public_transport_data.index(b)-1]) if (b in public_transport_data) else '-'
#         public_transport['subway']=int(public_transport_data[public_transport_data.index(s)-1]) if (s in public_transport_data) else '-'
#         public_transport['rail']=int(public_transport_data[public_transport_data.index(r)-1]) if (r in public_transport_data) else '-'
#         neighborhood_data['public transport']=public_transport

#         eating_drinking={}
#         # restaurants, bars and coffee shops
#         eating_drinking_string=soup.find('div', class_='block-eat-drink').find('div', class_='span12').text
#         eating_drinking_data=[int(i) for i in eating_drinking_string.replace(',', '').split() if i.isdigit()] 
#         eating_drinking['restaurants']=eating_drinking_data[0]
#         eating_drinking['shops']=eating_drinking_data[1]
#         eating_drinking['time']=eating_drinking_data[2]

#         neighborhood_data['eating drinking']=eating_drinking
        
#         walkscore_data.append(neighborhood_data)

#         line_count+=1
        
#     print(f'Processed {line_count} lines.')

# with open("walkscore.txt", 'w', encoding='utf-8') as f:
#     json.dump(walkscore_data, f, ensure_ascii=False, indent=4)


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

# PLOTS
# import numpy as np
# import matplotlib.mlab as mlab
# import matplotlib.pyplot as plt

# def gradeToValue(g):
#     switch = {
#         'A+': 96.67,
#         'A': 93.33,
#         'A-': 90.00,
#         'B+': 86.87,
#         'B': 83.33,
#         'B-': 80.00,
#         'C+': 76.67,
#         'C': 73.33,
#         'C-': 70.00,
#         'D': 65.00,
#         'F': 0.00
#     }
#     return switch.get(g, 0.0) 

# # rent=[]
# safety=[]
# overall=[]
# name=[]

# with open('/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/data/niche.json') as j:
#     data = json.load(j)
#     for d in data:
#         name.append(d["name"])
#         safety.append(gradeToValue(d["scores"]["Crime & Safety"]))
#         overall.append(gradeToValue(d["scores"]["Overall Grade"]))
#         # r=int(d["real estate"]["median rent"].replace('$','').replace(',',''))
#         # rent.append(r)

# # x = [21,22,23,4,5,6,77,8,9,10,31,32,33,34,35,36,37,18,49,50,100]
# # num_bins = 5
# # n, bins, patches = plt.hist(rent, facecolor='blue', alpha=0.5)
# # plt.xlabel('Rent')
# # plt.ylabel('Neighborhoods')
# # plt.title('Median Rent per Manhattan Neighborhood')
# # plt.show()

# # n, bins, patches = plt.hist(rent, facecolor='blue', alpha=0.5)
# # plt.xlabel('Rent')
# # plt.ylabel('Neighborhoods')
# # plt.title('Median Rent per Manhattan Neighborhood')
# # plt.show()

# fig, ax = plt.subplots()
# ax.scatter(overall, safety)

# all_points=set()
# new_names=[]
# new_points=[]

# for i, txt in enumerate(name):
#     point=(overall[i], safety[i])
#     if point not in all_points:
#         new_points.append(point)
#         all_points.add(point)
#         new_names.append(txt)
#     else:
#         new_names[new_points.index(point)]=new_names[new_points.index(point)] + ", " + txt

# for i,txt in enumerate(new_names):
#     plt.text(new_points[i][0]-.2, new_points[i][1]-.7, txt, va='bottom', fontsize=5, style='oblique', wrap=True)
#     # ax.annotate(txt, new_points[i], size=8)

# plt.xlabel('Overall Score')
# plt.ylabel('Safety Score')
# plt.title('Safety vs Overall Score per Manhattan Neighborhood')

# plt.show()


# COMPASS + STREETEASY

# url="https://www.compass.com/neighborhood-guides/nyc/battery-park-city/"
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, "html.parser")

# neighborhood_id=soup.find('div', class_='block-group')['class'][-1].split('-')[0]
# # print(soup)
# tags_data = soup.find('ul', class_='tags').find_all('li')

# neighborhood_data={}

# tags=[]
# for t in tags_data:
#     tags.append(t.text.lower())

# neighborhood_data['tags']=tags

# quickhits_classname=neighborhood_id+'-introQuickHitsContainer'
# quickhits_data = soup.find('div', class_=quickhits_classname).find_all('div', class_='textIntent-caption1')
# quickhits_labels=["WHAT TO EXPECT", "THE LIFESTYLE", "WHAT NOT TO EXPECT", "THE MARKET", "YOU'LL FALL IN LOVE WITH"]
# quickhits={}
# for (idx,l) in enumerate(quickhits_labels):
#     quickhits[l]=quickhits_data[idx*2+1].text.strip()
    
# neighborhood_data['quick hits']=quickhits

# nearestsubways=[]

# nearestsubways_classname=neighborhood_id+'-locationDetailsSubway'
# nearestsubways_data=soup.find('div', class_=nearestsubways_classname).find_all('img')
# for n in nearestsubways_data:
#     line_number=n['src'].split('/')[6].split('_transit.png')[0]
#     line={}
#     line['line']=line_number
#     line['img']=n['src']
#     nearestsubways.append(line)

# neighborhood_data['nearest subways']=nearestsubways

# commutetimes_data=soup.find('div', class_='commute--times').find_all('div')
# commutetimes={}
# for c in commutetimes_data:
#     dest=c.text.strip().split('\n')[0]
#     t=c.text.replace('m','').replace('h', '')
#     times=[int(i) for i in t.split() if i.isdigit()]
#     commutetimes[dest]={'train': times[0], 'car': times[1]}

# neighborhood_data['commute times']=commutetimes

# aroundtheblock_data=soup.find(id='around_the_block').find_all('div', class_='slide__inner__section')
# neighborhood_data['description']=aroundtheblock_data[0].find('div', class_='textIntent-body').text

# for (idx,c) in enumerate(aroundtheblock_data):
#     if idx==0:
#         continue
#     section_name=c.find('div', class_='textIntent-title1').text.strip().replace(':', '')
#     neighborhood_data[section_name]={'short': c.find('div', class_='textIntent-title2').text.strip(), 'long': c.find('div', class_='textIntent-body').text.strip()}

compass_data = []
with open('data/neighborhoods.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count+=1
            continue
        # elif line_count < 22:
        #     line_count+=1
        #     continue
        neighborhood_data={}
        neighborhood_data["id"]=row[0]
        neighborhood_data["name"]=row[1]
        if row[5]=="":
            continue
        neighborhood_data["compass url"]=row[5]
        url=row[5]
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        neighborhood_id=soup.find('div', class_='block-group')['class'][-1].split('-')[0]
        # print(soup)
        tags_data = soup.find('ul', class_='tags').find_all('li')

        tags=[]
        for t in tags_data:
            tags.append(t.text.lower())

        neighborhood_data['tags']=tags

        # quickhits_classname=neighborhood_id+'-introQuickHitsContainer'
        # quickhits_data = soup.find('div', class_=quickhits_classname).find_all('div', class_='textIntent-caption1')
        # quickhits_labels=["WHAT TO EXPECT", "THE LIFESTYLE", "WHAT NOT TO EXPECT", "THE MARKET", "YOU'LL FALL IN LOVE WITH"]
        # quickhits={}
        # for (idx,l) in enumerate(quickhits_labels):
        #     quickhits[l]=quickhits_data[idx*2+1].text.strip()
            
        # neighborhood_data['quick hits']=quickhits

        nearestsubways=[]

        nearestsubways_classname=neighborhood_id+'-locationDetailsSubway'
        nearestsubways_data=soup.find('div', class_=nearestsubways_classname).find_all('img')
        for n in nearestsubways_data:
            line_number=n['src'].split('/')[6].split('_transit.png')[0]
            line={}
            line['line']=line_number
            line['img']=n['src']
            nearestsubways.append(line)

        neighborhood_data['nearest subways']=nearestsubways

        commutetimes_data=soup.find('div', class_='commute--times').find_all('div')
        commutetimes={}
        for c in commutetimes_data:
            dest=c.text.strip().split('\n')[0]
            t=c.text.replace('m','').replace('h', '')
            times=[int(i) for i in t.split() if i.isdigit()]
            commutetimes[dest]={'train': times[0], 'car': times[1]}

        neighborhood_data['commute times']=commutetimes

        aroundtheblock_data=soup.find(id='around_the_block').find_all('div', class_='slide__inner__section')
        neighborhood_data['description']=aroundtheblock_data[0].find('div', class_='textIntent-body').text.strip()

        for (idx,c) in enumerate(aroundtheblock_data):
            if idx==0:
                continue
            section_name=c.find('div', class_='textIntent-title1').text.strip().replace(':', '')
            neighborhood_data[section_name]={'short': c.find('div', class_='textIntent-title2').text.strip(), 'long': c.find('div', class_='textIntent-body').text.strip()}

        compass_data.append(neighborhood_data)

with open("data/compass.txt", 'w', encoding='utf-8') as f:
    json.dump(compass_data, f, ensure_ascii=False, indent=4)

