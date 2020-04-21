from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.controllers.calculate import getTopNeighborhoods

project_name = "The Perfect Neighborhood"
net_id = "Stephanie Chang (sc2524), Kati Hsu (kyh24), Robert Zhang (rdz26), Sneha Kumar (sk2279), Shirley Kabir (szk4)"

@irsystem.route('/', methods=['POST'])
def search():
	age = ''
	commute_type = ''
	safety = ''
	budget = ''
	some = ''
	if request.method == 'POST':
		age = request.form["age"]
		commute_type = request.form["commute-type"]
		safety = request.form["safety"]
		budget=[int(b) for b in request.form.getlist('budget')]
		budget_min = int(((5000 - 0) / 100) *  int(min(budget)))
		budget_max = int(((5000 - 0) / 100) *  int(max(budget)))
		likes = request.form.getlist('likes')
	
	likes_string=""
	for l in likes:
		likes_string=likes_string + " " + l

	output_message = "Age: " + age + " Commute Type: " + commute_type + " Safety Priority: " + safety + " Budget: $" + str(budget_min) + "-" + str(budget_max) + " Activities: " + likes_string
	
	query={'age': age, 'commute-type': commute_type, 'safety': safety, 'budget-min': budget_min, 'budget-max': budget_max, 'likes': likes}

	data=getTopNeighborhoods(query)

	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

@irsystem.route('/', methods=['GET'])
def initial_search():
	data = []
	output_message=''
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
