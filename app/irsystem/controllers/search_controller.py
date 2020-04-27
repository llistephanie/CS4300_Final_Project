from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.controllers.calculate import getTopNeighborhoods

project_name = "The Perfect Neighborhood"
v1_link = "http://theperfectneighborhood-v1.herokuapp.com/"
net_id = "Stephanie Chang (sc2524), Kati Hsu (kyh24), Robert Zhang (rdz26), Sneha Kumar (sk2279), Shirley Kabir (szk4)"

@irsystem.route('/', methods=['POST'])
def search():
	if request.method == 'POST':
		age = request.form["age"]
		commute_type = request.form["commute-type"]
		commute_duration = request.form["commute-duration"]
		commute_destination = request.form["commute-destination"]

		budget_min=int(request.form["budget-min"])
		budget_max=int(request.form["budget-max"])
		likes = request.form.getlist('likes')

	likes_string=""
	for l in likes:
		likes_string=likes_string + " " + l

	output_message = "Age: " + age + " Commute Type: " + commute_type + " Budget: $" + str(budget_min) + "-" + str(budget_max) + " Activities: " + likes_string

	query={'age': age, 'commute-type': commute_type, 'commute-duration': commute_duration, 'commute-destination': commute_destination, 'budget-min': budget_min, 'budget-max': budget_max, 'likes': likes}

	print(query)

	print(query)

	data=getTopNeighborhoods(query)

	# print(data)

	return render_template('search.html', name=project_name, first_prototype = v1_link, netid=net_id, query=query, data=data)

@irsystem.route('/', methods=['GET'])
def initial_search():
	data = []
	output_message=''
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
