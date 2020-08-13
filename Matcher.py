from Consultant import Consultant
from Consultee import Consultee
from scipy.spatial.distance import cosine

class Matcher():

    # Initialize the data from the clean_file dataframe you get from app.py
    def __init__(self, data):
        self.initialData = data
        self.consultants = []
        self.consultees = []
        self.matched = {}
        self.not_matched = {}

    # Split up the consultants from the consultees
    def populate_initial_arrays(self):
        for index, row in self.initialData.iterrows():
            if (row['Role'] == "Consultant"):
                tempConsultant = Consultant(row)
                self.consultants.append(tempConsultant)
            if (row['Role'] == "Consultee"):
                tempConsultee = Consultee(row)
                self.consultees.append(tempConsultee)

    # Perform the actual matching algorithim
    def match(self):
        # Populate the initial arrays
        self.populate_initial_arrays()
        self.parsePeeps()

    def cosine_sim(self, cs, ct):
        major_sim = 1-cosine(cs.embedding[0], ct.embedding[0])
        goals_sim = 1-cosine(cs.embedding[1], ct.embedding[1])
        weights = [10, 1]
        avgs = [major_sim, goals_sim]

        for g in range(len(avgs)):
            avgs[g] = avgs[g] * weights[g] / sum(weights)
        rate = sum(avgs)

        return rate

    def parsePeeps(self):
        for consultant in self.consultants:
            consultant.createEmbedding()
        for consultee in self.consultees:
            consultee.createEmbedding()
