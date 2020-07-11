from Consultant import Consultant
from Consultee import Consultee
import math


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
        # Sort by previous consultants first
        self.check_previous_consultant()
        # Sort by major next
        self.sort_by_major()
        # After these matches have been made we can display the not_matched consultants/consultees
        # and let the user manually match them

    def check_previous_consultant(self):
        for cs in self.consultees:
            # Checks to see if any consultees requested a previous consultant
            if not math.isnan(cs.previous_consultant):
                """
                If the consultee has requested a previous consultant check to see if that consultant has
                signed up to be a consultant, if they have add to the dictionary matched keyed by Consultant:[Consultee]
                and remove them from self.consultees
                if the consultant has not signed up, push to dictionary not_matched keyed by Consultee/Consultant:REASON
                with REASON = "Consultee requested a previous consultant that has not signed up to be a consultant again"
                and remove them from self.consultees
                It's vital we remember to remove them or they will be assigned to another consultant again 
                """
                continue


    def sort_by_major(self):
        # Empty dictionary that will have the key = major, then the value = list of consultants/consultees
        major_consultant = {}
        major_consultee = {}
        # Populate the dictionaries
        for ct in self.consultants:
            if (ct.major in major_consultant):
                major_consultant[ct.major].append(ct)
            else:
                major_consultant[ct.major] = []
                major_consultant[ct.major].append(ct)
        for cs in self.consultees:
            if (cs.major in major_consultee):
                major_consultee[cs.major].append(cs)
            else:
                major_consultee[cs.major] = []
                major_consultee[cs.major].append(cs)

        # Using dictionary of major:[consultees] iterate through the various majors that consultees have
        # The consultants that have a major that no consultee has will be pushed to not_matched
        # with key = Consultant, value = "Consultant has a major ({}) that no consultee has".format
        for key in major_consultee:
            # If the major doesn't exist in the major:[consultants] dictionary then that means
            # no consultants exist for that consultee's major
            # We also need to take into account those that have an undecided major
            if (not key in major_consultant):
                for cs in major_consultee[key]:
                    self.not_matched[cs] = "Consultant does not exist with consultee's major ({}).".format(cs.major)
                    major_consultee[key].clear()
            else:
                # Match by gender preference first but there's no gender data point
                # Empty dictionary will be keyed by Consultant:number of consultees
                num_consultees = {}
                for ct in major_consultant[key]:
                    num_consultees[ct] = 0
                # Okay here's where I need to figure out the logic, there should be more
                # consultees than consultants right? So therefore we should be able to do some
                # simple math to find out how many consultees should be assigned to each consultant?
                # Then iterate over the consultants in the num_consultees dictionary, check how many have
                # already been assigned, then if they need one give them a consultee then remove the
                # consultee from the list.
                # I see a couple problems, we'll need to make sure we're removing the consultees so they
                # don't get assigned multiple times. Also we need to take into account the career goals
                # of the consultees and consultants. My thought is first sort by career goal then all the
                # undecided will be randomly assigned to those that have less consultees

        print(self.matched)
        print(self.not_matched)
