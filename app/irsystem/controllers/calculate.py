import json

# Full list of neighborhoods
# NOTE: if you use these as keys, you can simply update the shared data dictionary variable (data)

neighborhood_list = ['Battery Park',
                     'Chelsea',
                     'Chinatown',
                     'Civic Center',
                     'East Harlem',
                     'East Village',
                     'Financial District',
                     'Flatiron',
                     'Gramercy',
                     'Greenwich Village',
                     'Harlem',
                     "Hell's Kitchen",
                     'Inwood',
                     'Kips bay',
                     'Little Italy',
                     'Lower East Side',
                     'Marble Hill',
                     'Midtown',
                     'Morningside Heights',
                     'Murray Hill',
                     'Noho',
                     'Nolita',
                     'Roosevelt Island',
                     'Soho',
                     'Stuyvesant Town',
                     'Theater District',
                     'Tribeca',
                     'Two Bridges',
                     'Upper East Side',
                     'Upper West Side',
                     'Washington Heights',
                     'West Village']

"""
Shared data containing all the scores and information for each neighborhood.
Scores will be a value from 
Includes the following components:
    - description (of the neighborhood)
    - commute scores
    - safety/happiness score
    - budget
    - hobbies/interests
"""
data = {}
for x in neighborhood_list:
	data[x] = {}

def load_crime_and_descriptions():
	"""
	Function adds in the attributes "description" and "safety_score" for each neighborhood
	"""
	global data # declare global in order to update global data variable
	with open("data/safety.json","r") as f:
		input_data = json.load(f)

	data.update(input_data)

def main():
	"""
	Function will be loading all the data to update the global data variable
	"""
	load_crime_and_descriptions()

	print(data)

main()