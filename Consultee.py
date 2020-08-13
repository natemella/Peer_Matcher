import spacy
import numpy as np

class Consultee():
        def __init__(self, data):
            self.embedding = [0,0]
            self.role = data['Role']
            self.l_name = data['Last_Name']
            self.f_name = data['First_Name']
            self.email = data['Email']
            self.semesters = data['Semesters']
            self.number = data['Number']
            self.major = data['Major']
            self.major_semesters = data['Major_Semesters']
            self.career_goals = data['Career_Goals']
            self.career_goals_other = data['Career_Goals_Other']
            self.been_consultant = data['Been_Consultant']
            self.been_consultee = data['Been_Consultee']
            self.keep_consultant = data['Keep_Consultant']
            self.previous_consultant = data['Previous_Consultant']
            self.gender_preference = data['Gender_Preferenence']
            self.brag = data['Brag']
            self.no_life = data['No_Life']
            self.gain = data['Gain']
            self.gain_other = data['Gain_Other']
            self.consultant_consent = data['Consultant_Consent']
            self.consultee_consent = data['Consultee_Consent']
            self.club_consent = data['Club_Consent']
            self.commitment = data['Commitment']
            self.majors = {}
            self.career_goals_dict = {}

        def vec(self, s, nlp):
            return nlp(s).vector

        def createEmbedding(self):
            self.parseMajor()
            self.parseCareerGoals()

        def parseMajor(self):
            nlp = spacy.load("en_core_web_sm")
            major_vec = self.vec(self.major, nlp)
            self.embedding[0] = major_vec

        def parseCareerGoals(self):
            career_goal_list = self.career_goals.split(',')
            nlp = spacy.load("en_core_web_sm")
            doc_vec = np.zeros((96,))
            for cg in career_goal_list:
                temp_vec = self.vec(cg, nlp)
                doc_vec = np.add(doc_vec, temp_vec)
            self.embedding[1] = doc_vec