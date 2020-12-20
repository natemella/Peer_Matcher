import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from Matcher import Matcher
import copy

def path_to_list(path):
    folders = []
    while True:
        path, folder = os.path.split(path)
        if folder:
            folders.append(folder)
        else:
            if path:
                folders.append(path)
            break
    folders.reverse()
    return folders

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(294, 237)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.upload_button = QtWidgets.QPushButton(self.centralwidget)
        self.upload_button.setGeometry(QtCore.QRect(100, 50, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.upload_button.setFont(font)
        self.upload_button.setObjectName("upload_button")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 100, 251, 28))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.upload_button.resize(200, 50)
        self.upload_button.move(50, 50)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 294, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.upload_button.clicked.connect(self.upload)

        # THIS IS WHERE THE MAGIC HAPPENS
        self.pushButton_2.clicked.connect(self.print_path)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.upload_button.setText(_translate("MainWindow", "Upload here"))
        self.pushButton_2.setText(_translate("MainWindow", "Run Peer Matcher!"))

    def upload(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None)
        self.__myfile = fileName


    def __init__(self):
        self.__myfile =""


    def clean_data(self):
        data = pd.read_csv(self.__myfile, sep = '\t', encoding = "UTF-16")
        my_cols = [x for x in data.columns if x.startswith("Q")]
        clean_file = data[my_cols]
        clean_file.columns = clean_file.iloc[0]
        clean_file = clean_file[2::] # Skip first two lines of junk
        clean_file = clean_file[clean_file['First Name'].notna()]
        column_rename = {'Would you like to sign up to be a CONSULTANT or a CONSULTEE? (see definitions below)': "Role",
                         'First Name': "First_Name",
                         'Last Name': "Last_Name",
                         'Current Email Address (please double check to make sure you have entered it correctly)': "Email",
                         'Phone Number (please double check to make sure you have entered it correctly)': "Number",
                         'How many semesters have you completed at BYU?': "Semesters",
                         'What is your current major?': "Major",
                         'How many semesters have you been in your current major?': "Major_Semesters",
                         'What are your career goals? (Please choose all that apply.) - Selected Choice': "Career_Goals",
                         'What are your career goals? (Please choose all that apply.) - Other - Text': "Career_Goals_Other",
                         'Have you previously participated in the Life Sciences Peer Consulting Program as a CONSULTANT?': "Been_Consultant",
                         #'Have you previously participated in the Life Sciences Peer Consulting Program as a CONSULTEE?': "Been_Consultee",
                         'Do you have a consultant gender preference? - Selected Choice' : 'Gender_Pref',
                         'Would you like to retain your previous consultant? (Please note that your previous consultant may not have signed up for this semester. If that is the case, we will assign you a new one.)': "Keep_Consultant",
                         'Please enter the first AND last name of your previous consultant.': "Previous_Consultant",
                         'Do you have a consultant gender preference?': "Gender_Preferenence",
                         'Please share what skills and/or experience you believe qualify you to be a peer consultant.': "Brag",
                         'Will you be able to attend at least four of the five LFSCI 190R, Peer Consulting class meetings? The consultant training meeting and the kickoff event are mandatory. The meetings are as follows: 1. Consultant Training: Thursday, September 3rd at 5:00 pm in 2102 LSB 2. Kickoff Event: Thursday, September 10th at 5:00 pm in 2102 LSB3. Class Meeting 1: Thursday, October 1st at 5:00 pm in 2102 LSB4. Class Meeting 2: Thursday, October 22nd at 5:00 pm in 2102 LSB5. Class Meeting 3: Thursday, November 19th at 5:00 pm in 2102 LSB': "No_Life",
                         'What are you hoping to gain from your consultant this semester? (Please choose all that apply) - Selected Choice': "Gain",
                         'What are you hoping to gain from your consultant this semester? (Please choose all that apply) - Other - Text': "Gain_Other",
                         'I consent for my contact information to be released to my consultees.': "Consultant_Consent",
                         'I consent for my contact information to be released to my consultant.': "Consultee_Consent",
                         'I consent for my contact information to be released to clubs relevant to my major/career path.': "Club_Consent",
                         'Keeping in mind that my consultant is receiving training and earning credit for this experience, I commit to actively participate and regularly communicate with him/her.': "Commitment"}



        clean_file = clean_file.rename(columns = column_rename)
        clean_file['Role'] = [x.replace(" Consultant  (I have been in my CURRENT Life Sciences major for MORE than 3 semesters and would like to BE a Life Sciences Peer Consultant)","") for x in clean_file['Role']]
        clean_file['Role'] = [x.replace(" (I have been in my CURRENT Life Sciences major for FEWER than 3 semesters and would like to HAVE a Life Sciences Peer Consultant)","") for x in clean_file['Role']]
        peer_matcher = Matcher(clean_file)
        print("file cleaned")
        peer_matcher.match()
        print("NLP Parsing complete")

        # Make a dictionary where we map a combo (tuple) of consultant - consultees to a match score {tuple : float}
        my_matches = {}
        for ct in peer_matcher.consultants:
            for cs in peer_matcher.consultees:
                match_score = peer_matcher.cosine_sim(ct, cs)
                my_matches[(ct, cs)] = match_score

        # Make a list where we will store final matches
        final_matches = []

        # loop through our dictionary of potentials patches
        for x in list(my_matches):
            if len(my_matches) == 0:
                break
            # identify the best match
            current_max = max(my_matches.values())

            # Loop through dictionary of of matches to find the max
            for y in list(my_matches):
                if my_matches[y] == current_max:
                    # Remove the match from potential matches
                    my_matches.pop(y)
                    # Add the max to the list of final matches
                    final_matches.append(y)
                    ct = y[0]
                    ct.consultees.append(y[1])
                    cs = y[1]
                    cs.consultant = ct
                    break

            # Remove all current matches to this consultee
            consultee_to_remove = final_matches[-1][1]
            for x in list(my_matches):
                if x[1] == consultee_to_remove:
                    my_matches.pop(x)

            # If the consultant already has five matches, remove them
            consultant_to_remove = final_matches[-1][0]
            if len(consultant_to_remove.consultees) >= 15:
                for x in list(my_matches):
                    if x[0] == consultant_to_remove:
                        my_matches.pop(x)

            for x in list(my_matches):
                if x[0] == consultant_to_remove:
                    my_matches[x] -= 0.02

        print(final_matches)

        temp_output = open("temp_output.tsv", "w")

        temp_output.write("Consultant Email\tCareer Path\t"
                          "Other Career Path\tConsultee First Name\t"
                          "Consultee Last Name\tMajor\tCount\tConsultant Full Name"
                          "\tConsultee First Name\tConsultee Last Name\tConsultee Email"
                          "\tPhone Number\tMajor\tCareer Path\tOther Career Path"
                          "\tPrevious Consultant\tGender Preference\tDesired Help\tDesired Help Other\n")

        # Total Majors
        total_majors = set()
        for x in peer_matcher.consultants:
            if x.major not in total_majors:
                total_majors.add(x.major)

        for x in peer_matcher.consultees:
            if x.major not in total_majors:
                total_majors.add(x.major)

        for major in total_majors:
            major_consultants = [x for x in peer_matcher.consultants if x.major == major]
            major_consultees = [x for x in peer_matcher.consultees if x.major == major]

            num_consultants = len(major_consultants)
            nct = copy.copy(num_consultants)
            num_consultees = len(major_consultees)
            ncs = copy.copy(num_consultees)

            num_rows = copy.copy(max(num_consultants, num_consultees))
            for i in range(num_rows):
                if i < num_consultants:
                    ct = major_consultants[i]
                    ct_info = f'{ct.email}\t{ct.career_goals}\t{ct.career_goals_other}\t{ct.f_name}\t{ct.l_name}\t{ct.major}\t{len(ct.consultees)}\t'
                if i < num_consultees:
                    cs = major_consultees[i]
                    cs_info = f'{cs.consultant.f_name} {cs.consultant.l_name}\t{cs.f_name}\t{cs.l_name}\t{cs.email}\t{cs.number}\t{cs.major}\t' \
                            f'{cs.career_goals}\t{cs.career_goals_other}\t{cs.previous_consultant}\t' \
                            f'{cs.gender_preference}\t{cs.gain}\t{cs.gain_other}\n'
                if nct > 0 and ncs > 0:
                    temp_output.write(ct_info + cs_info)
                    nct -= 1
                    ncs -= 1
                elif nct > 0 and ncs == 0:
                    temp_output.write(ct_info + "\n")
                    nct -= 1
                elif ncs > 0 and nct == 0:
                    temp_output.write('\t\t\t\t\t\t\t' + cs_info)
                    ncs -= 1
        temp_output.close()
        df = pd.read_csv("temp_output.tsv", sep="\t")
        df.to_excel("Peer_Consulting_Matcher.xlsx")
        print("Done")



    # THIS IS WHERE MAIN CODE SHOULD GO.
    def print_path(self):
        if self.__myfile != "":
            print(self.__myfile)
            self.clean_data()





if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
