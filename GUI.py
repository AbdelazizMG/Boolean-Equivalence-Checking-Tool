from PyQt5 import QtWidgets , QtCore
from PyQt5 import uic

import sys , os , json


class UI_Window(QtWidgets.QMainWindow):

    #Constuctor
    def __init__(self):
            super(UI_Window,self).__init__()

            #load the UI file
            uic.loadUi("GUI.ui",self)

                                    #Entries
            self.__Exp1_Entry = self.findChild(QtWidgets.QLineEdit,"exp1_lineEdit")
            self.__Exp2_Entry = self.findChild(QtWidgets.QLineEdit,"exp2_lineEdit")  

                                    #Labels
            self.__Exp1Validation_label = self.findChild(QtWidgets.QLabel,"exp1Validation_label")   
            self.__Exp2Validation_label = self.findChild(QtWidgets.QLabel,"exp2Validation_label")  
            self.__Equivalence_label = self.findChild(QtWidgets.QLabel,"Equivalence_label")                                      

                                    #PushButtons
            self.__check_pushButton = self.findChild(QtWidgets.QPushButton,"check_pushButton")   

                                    #listWidget
            self.__dataBase_listwidget = self.findChild(QtWidgets.QListWidget,"dataBase_listWidget")                                                 

                                    #StatusBar
            self.__statusbar = self.findChild(QtWidgets.QStatusBar,"statusbar") 

                                    #Do Functionallity  
            self.__check_pushButton.clicked.connect( self.__Check)                                              

                                    #Variables  
            self.__projectDict = {     
                                 'trial': '',                        #Dict to hold the project information to be converted to json file
                                 'exp1' : '',
                                 'exp2' : '', 
                                 'result' : ''                                                             
                                 }                                    
            self.__dataBaseDirectory = "C:\Sondos"             #Variable to store the Data Base Directory Path 
            self.__baseDirectory = os.getcwd()                 #Variable to store cwd before changing any thing
            self.__projectsinDataBase = {} 
            self.__counter = 0

                                    #Statusbar Message
            self.__statusbar.showMessage("Welcome")    

                                    #Initial Action
            #Read Saved Projects at the beginning of the tool
            self.__readDataBase()

    #Function to Check the Equivalence of the two strings
    def __Check(self):
          self.__projectDict['exp1'] = self.__Exp1_Entry.text()
          self.__projectDict['exp2']  = self.__Exp2_Entry.text()
          self.__projectDict['result'] = str(True)
          self.__projectDict['trial'] = str(self.__counter)

          #Call Parser

          #Store Trial State
          self.__saveProject()

          #Clear Content
          self.__Exp1_Entry.setText('')
          self.__Exp2_Entry.setText('')

    #Function used to draw Project Content
    def __drawProject(self , firstExp , secondExp , Result):
        Verticalwidget = QtWidgets.QWidget()
        itemN = QtWidgets.QListWidgetItem()

        widgetFirstExp = QtWidgets.QLabel(f"Exp1 : {firstExp}")
        widgetSecondExp = QtWidgets.QLabel(f"Exp2 : {secondExp}")
        ResultValue = QtWidgets.QLabel(f"Equivalence : {Result}")

        widgetVLayout = QtWidgets.QVBoxLayout()
        widgetVLayout.addWidget(widgetFirstExp)
        widgetVLayout.addWidget(widgetSecondExp)
        widgetVLayout.addWidget(ResultValue)        
        widgetVLayout.addStretch()
      #  widgetVLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        Verticalwidget.setLayout(widgetVLayout)   
         
        itemN.setSizeHint(Verticalwidget.sizeHint())


        self.__dataBase_listwidget.addItem(itemN)
        self.__dataBase_listwidget.setItemWidget(itemN, Verticalwidget)        

    #Function to save the project content if it's true
    def __saveProject(self):

        os.chdir(self.__dataBaseDirectory)                   #Store Project Info in Data Base
        with open(f"{self.__counter}.json", "w") as outfile:
                        json.dump( self.__projectDict, outfile)                        

        os.chdir(self.__baseDirectory)                       #Return to current directory and draw new action 

        self.__drawProject(self.__projectDict['exp1'] , self.__projectDict['exp2'], self.__projectDict['result']) 

        self.__statusbar.showMessage(f"Trial '{self.__counter}' is created'")   

        self.__counter = self.__counter + 1
    
    #Function to read dataBase at the initial action of the tool
    def __readDataBase(self):
            if not os.path.exists(self.__dataBaseDirectory):  #Create Data Base Directory if it's first time to use the tool
                os.mkdir(self.__dataBaseDirectory)
            else:
                print("DATA BASE IS ALREADY CREATED")         #If not first time then read all projects in data base and show them  
                projects = os.listdir(self.__dataBaseDirectory)
                os.chdir(self.__dataBaseDirectory)   

            for project in projects:                          #Read Save Projects as JSON and store them in DICT
                prj = open(project) 
                prj_content =  json.load(prj)
                self.__projectsinDataBase[f"{prj_content['trial']}"] = prj_content

                self.__counter = int(prj_content['trial']) + 1      #Get the last number of trial used     

            os.chdir(self.__baseDirectory)                #Draw Projects
            for key in self.__projectsinDataBase.keys():
                self.__drawProject(self.__projectsinDataBase[key]['exp1'] , self.__projectsinDataBase[key]['exp2'], self.__projectsinDataBase[key]['result'])  

# Initialize The App
##################################################################################
if __name__ == "__main__":
   app = QtWidgets.QApplication(sys.argv)
   UIWindow = UI_Window()
   UIWindow.show()
   app.exec_()