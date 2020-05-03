# import pke

# # initialize keyphrase extraction model, here TopicRank
# extractor = pke.unsupervised.TopicRank()

# # load the content of the document, here document is expected to be in raw
# # format (i.e. a simple text file) and preprocessing is carried out using spacy
# extractor.load_document(input='/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/external_data/battery-park.txt', language='en')

# # keyphrase candidate selection, in the case of TopicRank: sequences of nouns
# # and adjectives (i.e. `(Noun|Adj)*`)
# extractor.candidate_selection()

# # candidate weighting, in the case of TopicRank: using a random walk algorithm
# extractor.candidate_weighting()

# # N-best selection, keyphrases contains the 10 highest scored candidates as
# # (keyphrase, score) tuples
# keyphrases = extractor.get_n_best(n=30)

# print(keyphrases)

# docker run liaad/yake:latest -ti "Battery Park City is a planned neighborhood of sleek high rises overlooking the Hudson River in downtown Manhattan. It has a secluded, quiet atmosphere but is only steps to the Financial District, which makes it a popular home for those working in the vicinity of Wall Street. Residents speak of the small-town vibe where \"all the parents know all the kids\". There are two synthetic-turf athletic fields used for baseball, softball, kickball, Frisbee, soccer, football, and lacrosse (mostly for children's use, although adults are welcome as well). A number of public parks provide grassy areas to soak up the sun on a warm day or just people watch.<br> The neighborhood has a number of cafes and restaurants, grocery stores and markets, and a shopping cinema with a food court and cinemas. The rich and powerful moor their boats at the neighborhood's North Cove Yacht Harbor, where you can also take sailing lessons.<br> Tribeca and the Financial District are just next door when you want to venture out of the area and a ferry service can whisk you across the river to New Jersey.<br> Battery Park City is bordered on the north by Tribeca, on the east by the Financial District, and on the south and west by the Hudson River."

from rake_nltk import Rake

r = Rake(min_length=1, max_length=2) # Uses stopwords for english from NLTK, and all puntuation characters.

with open('/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/external_data/battery-park.txt', 'r') as file:
    data = file.read().replace('\n', '')

data+="Battery Park offers high-quality schools, safe streets and greenspace galore. Residents stay active here.  Much of the social life takes place on the water, where you can catch Manhattan Yacht Club sailboats zipping by during races.  The condo towers of Battery Park City are within walking distance of Wall Street, making it a convenient place for financiers to live. What the neighborhood lacks in history it makes up for in quality of life.  The newly expanded Brookfield Place shopping center is a hub for restaurants, retail, and occasional concerts. "

data+="The housing stock in Battery Park City consists primarily of condos in newer developments.  These buildings offer plenty of perks and amenities, but they come at a price.  Sales and rentals here tend to be expensive."

r.extract_keywords_from_text(data)

print(r.get_ranked_phrases()[:20]) # To get keyword phrases ranked highest to lowest.

