import pandas as pd
import requests
import csv
import time
import os
import sys
import io
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from selenium.webdriver.common.action_chains import ActionChains
from PyQt5 import QtCore, QtGui, QtWidgets

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
        self.pushButton_2.clicked.connect(self.JOHNS_CODE)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.upload_button.setText(_translate("MainWindow", "Upload here"))
        self.pushButton_2.setText(_translate("MainWindow", "Run John Kreider\'s GoExpense tool"))

    def upload(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Receipt", "", "PDF receipts (*.pdf)")
        self.__myfile = fileName


    def __init__(self):
        self.__myfile =""


    # THIS IS WHERE MAIN CODE SHOULD GO.
    def JOHNS_CODE(self):
        if self.__myfile != "":
            print("YOU SUCCESSFULLY EXECUTED YOUR CODE JOHN!!")
            print(self.__myfile)
            oldFilePath = self.__myfile
            mylist = path_to_list(oldFilePath)
            newFilePath = os.path.join(*mylist)
            print("NEWFILE")
            print(newFilePath)

    # def runprogram


# This first def I pulled from somewhere online, basically it makes it so that the PDF is readable
def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text


# I load the receipt, but would LOVE to know how I can do this without hardcoding it

# receipt='C:\\Users\\45261\\Desktop\\expense app\\united receipt.pdf'
def the_tool(fileName):
    file = fileName
    receipt = os.path.abspath(fileName)
    total = (extract_text_from_pdf(receipt))

    # time.sleep(20)

    ticket_number = (re.search('[l][s](\d\d\d\d\d\d\d\d\d\d\d\d\d)', total).group(1))
    print(ticket_number)
    found = (re.search('[g][e](\d\d\d.\d\d)', total).group(1))
    print(found)
    price = "000" + found
    day = (re.search('[m][b][e][r]\d\d\d\d\d\d\d(\d+) (\w+) (\d+)', total).group(1))
    month = (re.search('[m][b][e][r]\d\d\d\d\d\d\d(\d+) (\w+) (\d+)', total).group(2))
    year = (re.search('[m][b][e][r]\d\d\d\d\d\d\d(\d+) (\w+) (\d+)', total).group(3))
    date = day + "-" + month + "-" + year
    print(date)
    type = "     Airfare"

    # Open up chrome
    driver = webdriver.Chrome()

    # Go to the GoExpense page
    driver.get('https://goexpense.bain.com/Expense/#/app/not-submitted')
    driver.maximize_window()

    # Click the "new item" button on GoExpense
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable(
        (By.XPATH, '/html/body/div[2]/div[2]/div[2]/ui-view/div//div[5]/div[2]/button'))).click()
    # new_item = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/ui-view/div//div[5]/div[2]/button")
    # new_item.click()
    # time.sleep(1)

    # Send the date to the calendar
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH,
                                                                '/html/body/div[2]/div[2]/div[2]/ui-view/div/div[5]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[3]/div[2]/input'))).send_keys(
        date)

    # This fills out the "type" portion
    Fly = driver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div[2]/ui-view/div/div[5]/div/div/div/div[2]/div/div/div/div[4]["ng-repeat"]')
    Fly.send_keys(type)
    Fly.click()
    Fly.send_keys(Keys.RETURN)

    # This adds the case code-I want to not hard code this is possible
    case = driver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div[2]/ui-view/div/div[5]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[5]["ng-repeat"]')
    time.sleep(1)
    ccode = "     D3MA"
    case.send_keys(ccode)
    case.send_keys(Keys.RETURN)

    # Send the money to the Local Amount area
    money = driver.find_element_by_xpath(
        "/html/body/div[2]/div[2]/div[2]/ui-view/div/div[5]/div/div/div/div[2]/div/div/div/div[9]")
    money.send_keys(price)
    money.send_keys(Keys.RETURN)

    # This uploads the receipt to them
    wait = WebDriverWait(driver, 10)
    element = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "div[ngf-drop]")))
    model = element.get_attribute("ng-model")
    file_input = driver.find_element_by_css_selector('input[ngf-drop]')
    file_input.send_keys(receipt)

    # this clicks into Destination so that you can just type it in and go
    destination = driver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div[2]/ui-view/div/div[5]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[1]/div/div/div/textarea')
    destination.click()

    ticknum = driver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div[2]/ui-view/div/div[5]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/div/div[1]/div/div/div/textarea')
    ticknum.send_keys(ticket_number)

    time.sleep(20)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
