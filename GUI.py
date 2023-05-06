from PyQt5 import QtWidgets , QtCore , QtGui
from PyQt5 import uic

from node import node
from Parser import Parser
from BDD import BDD
from ROBDD import ROBDD
from drawer import Drawer
from Checker import Equivalence_Checker

import sys , os , json

class UI_Window(QtWidgets.QMainWindow):

    #Constuctor
    def __init__(self):
            super(UI_Window,self).__init__()

            #Define Other Widgets
            self.__BDD = BDD()
            self.__Checker = Equivalence_Checker()
            self.__drawer = Drawer()

            #load the UI file
            uic.loadUi("GUI.ui",self)

                                    #Entries
            self.__Exp1_Entry = self.findChild(QtWidgets.QLineEdit,"exp1_lineEdit")
            self.__Exp2_Entry = self.findChild(QtWidgets.QLineEdit,"exp2_lineEdit")  

                                    #Labels
            self.__Exp1Validation_label = self.findChild(QtWidgets.QLabel,"exp1Validation_label")   
            self.__Exp2Validation_label = self.findChild(QtWidgets.QLabel,"exp2Validation_label")  
            self.__Equivalence_label = self.findChild(QtWidgets.QLabel,"Equivalence_label")                                      
            self.__BDD_1_image = self.findChild(QtWidgets.QLabel,"BDD_image_1")
            self.__BDD_2_image = self.findChild(QtWidgets.QLabel,"BDD_image_2")
            self.__ROBDD_1_image = self.findChild(QtWidgets.QLabel,"ROBDD_image1")
            self.__ROBDD_2_image = self.findChild(QtWidgets.QLabel,"ROBDD_image2")

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
                                 'exp1_valid' : 0 ,
                                 'exp2_valid' : 0 , 
                                 'valid': '0', 
                                 'result' : ''                                                             
                                 }                                    
            self.__dataBaseDirectory = "C:\Sondos"             #Variable to store the Data Base Directory Path 
            self.__baseDirectory = os.getcwd()                 #Variable to store cwd before changing any thing
            self.__projectsinDataBase = {} 
            self.__counter = 0
            self.__exp1validation = 0

            self.__parser = Parser()

                                    #Statusbar Message
            self.__statusbar.showMessage("Welcome")    

                                    #Initial Action
            #Read Saved Projects at the beginning of the tool
            self.__readDataBase()

    #Function to Check the Equivalence of the two strings
    def __Check(self):

          #Read Entry
          if self.__Exp1_Entry.text() == "" or self.__Exp1_Entry.text() == "":
                return
          
          self.__projectDict['exp1'] = self.__Exp1_Entry.text()
          self.__projectDict['exp2']  = self.__Exp2_Entry.text()
          self.__projectDict['trial'] = str(self.__counter)

          #Call Parser
          flag_barcket,vars_flag,expr_flag,error_list_names,variable_list1,input_exp1 = self.__parser.GUI_check(self.__projectDict['exp1'])

          self.__Exp1Validation_label.setStyleSheet("color: red;")  
          if flag_barcket == 0:
                self.__Exp1Validation_label.setText('There is an error in Brackets ')
          elif vars_flag == 0:
                self.__Exp1Validation_label.setText(f'Variables {error_list_names} are invalid ')
          elif expr_flag == 0:
                self.__Exp1Validation_label.setText('There is an error in Expression ')
          else:
                self.__Exp1Validation_label.setText('VALID ') 
                self.__Exp1Validation_label.setStyleSheet("color: green;")
                self.__projectDict['exp1_valid'] = '1'    

          flag_barcket,vars_flag,expr_flag,error_list_names,variable_list2,input_exp2 = self.__parser.GUI_check(self.__projectDict['exp2'])


           
          if flag_barcket == 0:
                self.__Exp2Validation_label.setText('There is an error in Brackets ')
                self.__Exp2Validation_label.setStyleSheet("color: red;") 
          elif vars_flag == 0:
                self.__Exp2Validation_label.setText(f'Variables {error_list_names} are invalid ')
                self.__Exp2Validation_label.setStyleSheet("color: red;") 
          elif expr_flag == 0:
                self.__Exp2Validation_label.setText('There is an error in Expression ')
                self.__Exp2Validation_label.setStyleSheet("color: red;") 
          else:
                self.__Exp2Validation_label.setText('VALID ') 
                self.__Exp2Validation_label.setStyleSheet("color: green;")  
                self.__projectDict['exp2_valid'] = '1'                

          if self.__projectDict['exp1_valid'] == '1' and self.__projectDict['exp2_valid'] == '1':

            #Store Trial State
            self.__saveProject()

            #Exp1 Operation   
            variable_list1_drawable , TT_1_drawable = self.__parser.Parser_Output(input_exp1,variable_list1)
            list1_drawable = self.__BDD.start(variable_list1_drawable,TT_1_drawable)

            self.__drawer.draw(list1_drawable)

            flag_barcket,vars_flag,expr_flag,error_list_names,variable_list1,input_exp1 = self.__parser.GUI_check(self.__projectDict['exp1'])
            variable_list1 , TT_1_p = self.__parser.Parser_Output(input_exp1,variable_list1)            
            list1 = self.__BDD.start(variable_list1,TT_1_p)
            list1.reverse()
            self.__ROBDD1 = ROBDD(len(variable_list1))
            labelled_list1 = self.__ROBDD1.assign_labels(list1)
           
            Reduced_List1= [node(0, 0), node(1, 1)]
            list11 = self.__ROBDD1.Remove_Nodes(labelled_list1, Reduced_List1)
            list11.reverse()
            self.__drawer.draw(list11)

            #Exp2 Operation
            variable_list2_drawable , TT_2_drawable = self.__parser.Parser_Output(input_exp2,variable_list2)
            list2_drawable = self.__BDD.start(variable_list2_drawable,TT_2_drawable)
            self.__drawer.draw(list2_drawable)

            flag_barcket,vars_flag,expr_flag,error_list_names,variable_list2,input_exp2 = self.__parser.GUI_check(self.__projectDict['exp2'])
            variable_list2 , TT_2_p = self.__parser.Parser_Output(input_exp2,variable_list2)
            list2 = self.__BDD.start(variable_list2,TT_2_p)
            list2.reverse()
            self.__ROBDD2 = ROBDD(len(variable_list2))
            labelled_list2 = self.__ROBDD2.assign_labels(list2)
            Reduced_List2= [node(0, 0), node(1, 1)]
            list2 = self.__ROBDD2.Remove_Nodes(labelled_list2, Reduced_List2)
            list2.reverse()
            self.__drawer.draw(list2)

            #######################################
            flag_barcket,vars_flag,expr_flag,error_list_names,variable_list1,input_exp1 = self.__parser.GUI_check(self.__projectDict['exp1'])
            variable_list1 , TT_1_p = self.__parser.Parser_Output(input_exp1,variable_list1)            
            list1 = self.__BDD.start(variable_list1,TT_1_p)
            list1.reverse()
            self.__ROBDD1 = ROBDD(len(variable_list1))
            labelled_list1 = self.__ROBDD1.assign_labels(list1)
           
            Reduced_List1= [node(0, 0), node(1, 1)]
            list11 = self.__ROBDD1.Remove_Nodes(labelled_list1, Reduced_List1)
            list11.reverse()
            ##############################################################
            flag_barcket,vars_flag,expr_flag,error_list_names,variable_list2,input_exp2 = self.__parser.GUI_check(self.__projectDict['exp2'])
            variable_list2 , TT_2_p = self.__parser.Parser_Output(input_exp2,variable_list2)
            list2 = self.__BDD.start(variable_list2,TT_2_p)
            list2.reverse()
            self.__ROBDD2 = ROBDD(len(variable_list2))
            labelled_list2 = self.__ROBDD2.assign_labels(list2)
            Reduced_List2= [node(0, 0), node(1, 1)]
            list2 = self.__ROBDD2.Remove_Nodes(labelled_list2, Reduced_List2)
            list2.reverse()
            ###################################################################
            if self.__Checker.start(list11,list2,variable_list1,variable_list2) :           
              self.__Equivalence_label.setText("Equivalent") 
              self.__Equivalence_label.setStyleSheet("color: green;")  

            else:
              self.__Equivalence_label.setText("Non-Equivalent") 
              self.__Equivalence_label.setStyleSheet("color: red;")  

                                    
            self.__projectDict['result'] = self.__Equivalence_label.text()



            #SHOW RESULT


            #DRAW IMAGES
            pixmap = QtGui.QPixmap('graph0.png')
            self.__BDD_1_image.setPixmap(pixmap)
            self.__BDD_1_image.setScaledContents(True)
            pixmap = QtGui.QPixmap('graph2.png')
            self.__BDD_2_image.setPixmap(pixmap)
            self.__BDD_2_image.setScaledContents(True)
            pixmap = QtGui.QPixmap('graph1.png')
            self.__ROBDD_1_image.setPixmap(pixmap)
            self.__ROBDD_1_image.setScaledContents(True)
            pixmap = QtGui.QPixmap('graph3.png')
            self.__ROBDD_2_image.setPixmap(pixmap)
            self.__ROBDD_2_image.setScaledContents(True)

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