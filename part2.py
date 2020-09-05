import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from Matcher import Matcher
import copy
import xdrlib

def remove_duplicates(df):
    if True in df.Q4.duplicated():
        print("\nFound Duplicates!!!\n")
        print([df.Q4.values[i] for i in range(0, len(df.Q4.duplicated())) if
               df.Q4.duplicated()[i] == True])
        print()
        df = df.loc[~(df.Q4.duplicated())]
        return df
    else:
        return df



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

myFiles = []

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
        self.pushButton_2.setText(_translate("MainWindow", "Run Peer Matcher Part 2!"))

    def upload(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None)
        self.__myfile = fileName

    def clean_data(self):
        None

    # THIS IS WHERE MAIN CODE SHOULD GO.
    def print_path(self):
        if self.__myfile != "":
            print(self.__myfile)
            self.clean_data()
            input = self.__myfile

            outputdir = os.path.join(*path_to_list(input)[:-1])
            output = os.path.join(*[outputdir, "Peer_Consulting_Part2.tsv"])

            consultant_email = {}

            assignments = {}

            consultee_info = {}

            df = pd.read_excel(input)
            df = df.fillna("")

            max_size =0

            for index, row in df.iterrows():
                # hard coded
                consultant = row["Consultant Full Name"]
                if consultant != "" :
                    assignments[consultant] = []

            for index, row in df.iterrows():
                full_name = f'{row["Consultant First Name"]} {row["Consultant Last Name"]}'
                full_name = full_name.replace("  "," ")
                email = row["Consultant Email"]
                consultant = row["Consultant Full Name"]
                consultant = consultant.replace("  ", " ")
                consultee_full_name = f'{row["Consultee First Name"]} {row["Consultee Last Name"]}'

                if email != "":
                    consultant_email[full_name] = email

                if consultant != "":
                    assignments[consultant].append(consultee_full_name)
                    if len(assignments[consultant]) > max_size:
                        max_size = len(assignments[consultant])

                consultee_info[consultee_full_name] = df.loc[index,['Consultee Email','Phone Number',
                                                           'Major.1', 'Career Path.1','Other Career Path.1',
                                                           'Previous Consultant','Gender Preference','Desired Help',
                                                           'Desired Help Other']]

            with open(output, 'w', encoding='utf-8') as out:
                out.write("Consultant First Name\tConsultant Last Name\tEmail\t")
                myString = ""
                for i in range(1, max_size +1):
                    myString += f'Consultee_{i}_Name\tConsultee_{i}_Email\tConsultee_{i}_Number\tConsultee_{i}_Major\t' \
                                f'Consultee_{i}_CareerPath\tConsultee_{i}_CareerPathOther\tConsultee_{i}_Former_Consultant\t' \
                                f'Consultee_{i}_Gender_Preference\tConsultee_{i}_DesiredHelp\tConsultee_{i}_DesiredHelpOther\t'
                myString = myString[:-1]
                out.write(f'{myString}\n')
                for consultant in consultant_email:
                    consultant = consultant.replace("  ", " ")
                    myString =""
                    name_to_list = consultant.split(" ")
                    num_of_names = len(name_to_list)
                    myString += (f'{name_to_list[0]}\t')
                    myString += " ".join(name_to_list[1:num_of_names])
                    myString += (f"\t{consultant_email[consultant]}\t")
                    total_assignments = assignments[consultant]
                    for one_consultee in total_assignments:
                        info = consultee_info[one_consultee]
                        myString += (f'{one_consultee}\t')
                        for value in info:
                            myString += (f'{value}\t')
                    out.write(f'{myString[:-1]}\n')

            df = pd.read_csv(output, sep='\t')
            df.to_excel(output.replace("tsv","xlsx"), index=False)
            os.remove(output)


    def __init__(self):
        self.__myfile =""


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


    #
