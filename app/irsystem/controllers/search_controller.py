from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "The Perfect Neighborhood"
net_id = "Stephanie Chang (sc2524), Kati Hsu (kyh24), Robert Zhang (rdz26), Sneha Kumar (sk2279), Shirley Kabir (szk4)"

@irsystem.route('/', methods=['POST','GET'])
def search():
	if request.method == 'POST':
		age = request.form["age"]
		commute_type = request.form["commute-type"]
		safety = request.form["safety"]
		budget = request.form["budget"]
		some = request.form["some"]
	else:
		age = request.args.get('age')
		commute_type = request.args.get('commute-type')
		safety = request.args.get('safety')
		budget = request.args.get('budget')
		some = request.args.get('some')

	if not age:
		data = []
		output_message = ''
	else:
		output_message = "Your age: " + age + " Commute: " + commute_type + " Safety: " + safety + " Budget: " + budget + " Some: " + some
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
