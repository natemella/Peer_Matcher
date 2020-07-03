import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
import os

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


    # THIS IS WHERE MAIN CODE SHOULD GO.
    def print_path(self):
        if self.__myfile != "":
            print(self.__myfile)



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
