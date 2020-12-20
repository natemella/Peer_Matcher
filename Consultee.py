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
            # self.been_consultee = data['Been_Consultee']
            # self.keep_consultant = data['Keep_Consultant']
            self.previous_consultant = "NAN"
            self.gender_preference = data['Gender_Pref']
            # self.brag = data['Brag']
            # try:
            #     self.no_life = data['No_Life']
            # except Exception:
            #     self.no_life = ""
            # try:
            self.gain = data['Gain']
            # except Exception:
            #     self.gain = ""
            # try:
            self.gain_other = data['Gain_Other']
            # except Exception:
            #     self.gain_other = ""
            # try:
            #     self.consultant_consent = data['Consultant_Consent']
            # except Exception:
            #     self.consultant_consent = ""
            # try:
            #     self.consultee_consent = data['Consultee_Consent']
            # except Exception:
            #     self.consultant_consent = ""
            # try:
            #     self.club_consent = data['Club_Consent']
            # except Exception:
            #     self.club_consent = ""
            # try:
            #     self.commitment = data['Commitment']
            # except Exception:
            #     self.commitment = ""
            self.majors = {}
            self.career_goals_dict = {}
            self.consultant = ''

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