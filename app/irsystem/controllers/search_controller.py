from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.controllers.calculate import getTopNeighborhoods
import os

project_name = "The Perfect Neighborhood"
v1_link = "http://theperfectneighborhood-v1.herokuapp.com/"
net_id = "Stephanie Chang (sc2524), Kati Hsu (kyh24), Robert Zhang (rdz26), Sneha Kumar (sk2279), Shirley Kabir (szk4)"

subways = {'1': {'name': 'Broadway–Seventh Avenue Local', 'img': 'static/subways/1.svg', 'color': '#ee352e'}, '2': {'name': 'Seventh Avenue Express', 'img': 'static/subways/2.svg', 'color': '#ee352e'}, '3': {'name': 'Seventh Avenue Express', 'img': 'static/subways/3.svg', 'color': '#ee352e'}, '4': {'name': 'Lexington Avenue Express', 'img': 'static/subways/4.svg', 'color': '#00933c'}, '5': {'name': 'Lexington Avenue Express', 'img': 'static/subways/5.svg', 'color': '#00933c'}, '6': {'name': 'Lexington Avenue Local', 'img': 'static/subways/6.svg', 'color': '#00933c'}, '6d': {'name': 'Pelham Bay Park Express', 'img': 'static/subways/6d.svg', 'color': '#00933c'}, '7': {'name': 'Flushing Local', 'img': 'static/subways/7.svg', 'color': '#b933ad'}, '7d': {'name': 'Flushing Express', 'img': 'static/subways/7d.svg', 'color': '#b933ad'}, 's': {'name': '42nd Street Shuttle', 'img': 'static/subways/s.svg', 'color': '#808184'}, 'a': {'name': 'Eighth Avenue Express', 'img': 'static/subways/a.svg', 'color': '#0039A6'}, 'b': {'name': 'Sixth Avenue Express', 'img': 'static/subways/b.svg', 'color': '#ff6319'}, 'c': {'name': 'Eighth Avenue Local', 'img': 'static/subways/c.svg', 'color': '#0039A6'}, 'd': {'name': 'Sixth Avenue Express', 'img': 'static/subways/d.svg', 'color': '#ff6319'}, 'e': {'name': 'Eighth Avenue Local', 'img': 'static/subways/e.svg', 'color': '#0039A6'}, 'f': {'name': 'Queens Boulevard Express/Sixth Avenue Local', 'img': 'static/subways/f.svg', 'color': '#ff6319'}, 'g': {'name': 'Brooklyn–Queens Crosstown', 'img': 'static/subways/g.svg', 'color': '#6cbe45'}, 'j': {'name': 'Nassau Street Local', 'img': 'static/subways/j.svg', 'color': '#996633'}, 'l': {'name': '14th Street–Canarsie Local', 'img': 'static/subways/l.svg', 'color': '#a7a9ac'}, 'm': {'name': 'Queens Boulevard/Sixth Avenue Local', 'img': 'static/subways/m.svg', 'color': '#ff6319'}, 'n': {'name': 'Broadway Express', 'img': 'static/subways/n.svg', 'color': '#fccc0a'}, 'q': {'name': 'Second Avenue/Broadway Express/Brighton Local', 'img': 'static/subways/q.svg', 'color': '#00add0'}, 'r': {'name': 'Broadway Local', 'img': 'static/subways/r.svg', 'color': '#fccc0a'}, 'sf': {'name': 'Franklin Avenue Shuttle', 'img': 'static/subways/sf.svg', 'color': '#808184'}, 'sr': {'name': 'Rockaway Park Shuttle', 'img': 'static/subways/sr.svg', 'color': '#808184'}, 'w': {'name': 'Broadway Local', 'img': 'static/subways/w.svg', 'color': '#fccc0a'}, 'z': {'name': 'Nassau Street Express', 'img': 'static/subways/z.svg', 'color': '#808184'}}


@irsystem.route('/', methods=['POST'])
def search():
    if request.method == 'POST':
        age = request.form["age"]
        commute_type = request.form["commute-type"]
        commute_duration = request.form["commute-duration"]
        commute_destination = request.form["commute-destination"]

        subway_service = request.form["subway-service"]

        number_beds = request.form["number-beds"]
        budget_min = int(request.form["budget-min"])
        budget_max = int(request.form["budget-max"])

        likes = request.form.getlist('likes')

    query = {'age': age, 'commute-type': commute_type, 'commute-duration': commute_duration,
             'commute-destination': commute_destination, 'number-beds': number_beds, 'budget-min': budget_min, 'budget-max': budget_max, 'likes': likes, 'subway-service': subway_service}

    data, valid_queries = getTopNeighborhoods(query)
    return render_template('search.html', name=project_name, first_prototype=v1_link, netid=net_id, query=query, data=data, subways=subways, valid_queries=str(len(valid_queries)>0))


@irsystem.route('/', methods=['GET'])
def initial_search():
    data = []
    output_message = ''
    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, subways=subways)
