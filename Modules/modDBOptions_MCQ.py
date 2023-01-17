##  This file has a class of giving the main screen for making MySQL connections, creating and dropping database and tables.
##  Exporting MCQs text and images, only images and give the option to go to the G1 Quiz screen.

import tkinter as tk
from tkinter import messagebox
import os
import modConMySQL_MCQ
import modDBTabCrDr_MCQ
import modExpData_MCQ
import modExpData_Images
import modStartQuiz_MCQ

class ClassDBOptions:
#Starting Function********************************************#    
    def __init__(self, para_master):
        self.master = para_master
        self.master.geometry()
        self.master.resizable(0,0)
        self.master.title("G1 Test - Database Options") #Show title
        self.master.conHost = ""
        self.master.conUser = ""
        self.master.conPassword = ""
        self.objCrDr = modDBTabCrDr_MCQ.ClassDBTabCrDr()
        #self.objExpData_MCQ = modExpData_MCQ.ClassExportData_MCQ()
        self.strWinTitle = "G1 Test"
        dbOptionsFrame = []
        btnList = []
        btnListString = ["Exit","Connect MySQL","Drop Database","Create Database","Drop MCQ Table","Create MCQ Table","Drop Images Table","Create Images Table","Drop Quiz Tables","Create Quiz Tables","Export Signs MCQs","Export Rules MCQs","Export Images","G1 Quiz"]
        dbOptionsFrame.append(tk.Frame(self.master))
        dbOptionsFrame[0].grid(row=0)
        lblHeading = tk.Label(dbOptionsFrame[0], text = "G1 Test - Database Options", font=('arial',20,'bold'),
                             width=34,padx=8,pady=16,bd=8,fg="Cornsilk", bg='cadet blue',)
        lblHeading.grid(row=0)
        for intBtnCounter in range(14):
            dbOptionsFrame.append(tk.Frame(self.master))
            dbOptionsFrame[int(intBtnCounter/2)+1].grid(row=int(intBtnCounter/2)+1,columnspan=2)
            btnList.append(tk.Button(dbOptionsFrame[int(intBtnCounter/2)+1],text = btnListString[intBtnCounter], font=('arial',16,'bold'),
                                  width=20,padx=4,pady=8,bd=16,fg="blue", bg='powder blue',))
            btnList[intBtnCounter].grid(row=int(intBtnCounter/2)+1,column=intBtnCounter%2+1)
        btnList[0].config(fg="red",bg='gold')
        list(map(lambda intVal: btnList[btnListString.index(intVal)].config(command=lambda:self.btnClicked(intVal)), btnListString))
#Ending Function**********************************************#
#Starting Function********************************************#
    def btnClicked(self,paraBtn):
        try:
            if paraBtn=="Exit":
                msgBoxQ = messagebox.askquestion(self.strWinTitle + ' - Exit Application','Are you sure you want to exit the "G1 Test" program?',icon = 'warning') 
                if msgBoxQ == 'yes':
                    os._exit(0)
            elif paraBtn=="Connect MySQL":
                self.fn_getMySQLConnection("")
            elif paraBtn=="Drop Database":
                if self.master.conHost=="" and self.master.conUser=="" and self.master.conPassword=="":
                    self.fn_getMySQLConnection(" Then drop the database!")
                elif self.master.conHost!="" and self.master.conUser!="" and self.master.conPassword!="":
                    self.objCrDr.fn_setHostUserPassword(self.master.conHost,self.master.conUser,self.master.conPassword)
                    self.objCrDr.fn_DrDB()
            elif paraBtn=="Create Database":
                if self.master.conHost=="" and self.master.conUser=="" and self.master.conPassword=="":
                    self.fn_getMySQLConnection(" Then create the database!")
                elif self.master.conHost!="" and self.master.conUser!="" and self.master.conPassword!="":
                    self.objCrDr.fn_setHostUserPassword(self.master.conHost,self.master.conUser,self.master.conPassword)
                    self.objCrDr.fn_CrDB()
            elif paraBtn=="Drop MCQ Table":
                if self.master.conHost=="" and self.master.conUser=="" and self.master.conPassword=="":
                    self.fn_getMySQLConnection(" Then drop the table!")
                elif self.master.conHost!="" and self.master.conUser!="" and self.master.conPassword!="":
                    self.objCrDr.fn_setHostUserPassword(self.master.conHost,self.master.conUser,self.master.conPassword)
                    self.objCrDr.fn_DrTB_MCQ()
            elif paraBtn=="Create MCQ Table":
                if self.master.conHost=="" and self.master.conUser=="" and self.master.conPassword=="":
                    self.fn_getMySQLConnection(" Then create the table!")
                elif self.master.conHost!="" and self.master.conUser!="" and self.master.conPassword!="":
                    self.objCrDr.fn_setHostUserPassword(self.master.conHost,self.master.conUser,self.master.conPassword)
                    self.objCrDr.fn_CrTB_MCQ()
            elif paraBtn=="Drop Images Table":
                if self.master.conHost=="" and self.master.conUser=="" and self.master.conPassword=="":
                    self.fn_getMySQLConnection(" Then drop the table!")
                elif self.master.conHost!="" and self.master.conUser!="" and self.master.conPassword!="":
                    self.objCrDr.fn_setHostUserPassword(self.master.conHost,self.master.conUser,self.master.conPassword)
                    self.objCrDr.fn_DrTB_Images()
            elif paraBtn=="Create Images Table":
                if self.master.conHost=="" and self.master.conUser=="" and self.master.conPassword=="":
                    self.fn_getMySQLConnection(" Then create the table!")
                elif self.master.conHost!="" and self.master.conUser!="" and self.master.conPassword!="":
                    self.objCrDr.fn_setHostUserPassword(self.master.conHost,self.master.conUser,self.master.conPassword)
                    self.objCrDr.fn_CrTB_Images()
            elif paraBtn=="Drop Quiz Tables":
                if self.master.conHost=="" and self.master.conUser=="" and self.master.conPassword=="":
                    self.fn_getMySQLConnection(" Then drop the tables!")
                elif self.master.conHost!="" and self.master.conUser!="" and self.master.conPassword!="":
                    self.objCrDr.fn_setHostUserPassword(self.master.conHost,self.master.conUser,self.master.conPassword)
                    self.objCrDr.fn_DrTB_Quiz()
            elif paraBtn=="Create Quiz Tables":
                if self.master.conHost=="" and self.master.conUser=="" and self.master.conPassword=="":
                    self.fn_getMySQLConnection(" Then create the tables!")
                elif self.master.conHost!="" and self.master.conUser!="" and self.master.conPassword!="":
                    self.objCrDr.fn_setHostUserPassword(self.master.conHost,self.master.conUser,self.master.conPassword)
                    self.objCrDr.fn_CrTB_Quiz()
            elif paraBtn=="Export Signs MCQs":
                if self.master.conHost=="" and self.master.conUser=="" and self.master.conPassword=="":
                    self.fn_getMySQLConnection(" Then Export Data of Signs MCQs!")
                elif self.master.conHost!="" and self.master.conUser!="" and self.master.conPassword!="":
                    self.fn_exportData_MCQ(1)
            elif paraBtn=="Export Rules MCQs":
                if self.master.conHost=="" and self.master.conUser=="" and self.master.conPassword=="":
                    self.fn_getMySQLConnection(" Then Export Data of Rules MCQs!")
                elif self.master.conHost!="" and self.master.conUser!="" and self.master.conPassword!="":
                    self.fn_exportData_MCQ(2)
            elif paraBtn=="Export Images":
                if self.master.conHost=="" and self.master.conUser=="" and self.master.conPassword=="":
                    self.fn_getMySQLConnection(" Then Export Images!")
                elif self.master.conHost!="" and self.master.conUser!="" and self.master.conPassword!="":
                    self.fn_exportData_Images()
            elif paraBtn=="G1 Quiz":
                if self.master.conHost=="" and self.master.conUser=="" and self.master.conPassword=="":
                    self.fn_getMySQLConnection(" Then start G1 Quiz!")
                elif self.master.conHost!="" and self.master.conUser!="" and self.master.conPassword!="":
                    self.fn_StartQuiz_MCQ()
        except:
            messagebox.showinfo(self.strWinTitle,'Exception occured! {}'.format(e))
#Ending Function**********************************************#
#Starting Function********************************************#
    def fn_getMySQLConnection(self,para_Message1):
        messagebox.showinfo(self.strWinTitle,'Please set valid entries of Host, User and Password to get MySQL connection!' + para_Message1)
        self.master.withdraw()
        self.SlaveWindow = tk.Toplevel(self.master)
        #self.ChildWindow.geometry('350x350')
        self.appCnMySQL = modConMySQL_MCQ.ClassConnectMySQL(self.master,self.SlaveWindow)
#Ending Function**********************************************#
#Starting Function********************************************#
    def fn_exportData_MCQ(self,para_MCQType):
        self.master.withdraw()
        self.SlaveWindow = tk.Toplevel(self.master)
        #self.ChildWindow.geometry('350x350')
        self.appExpMCQ = modExpData_MCQ.ClassExportData_MCQ(self.master,self.SlaveWindow,para_MCQType)
#Ending Function**********************************************#
#Starting Function********************************************#
    def fn_exportData_Images(self):
        self.master.withdraw()
        self.SlaveWindow = tk.Toplevel(self.master)
        #self.ChildWindow.geometry('350x350')
        self.appExpImages = modExpData_Images.ClassExportData_Images(self.master,self.SlaveWindow)
#Ending Function**********************************************#
#Starting Function********************************************#
    def fn_StartQuiz_MCQ(self):
        self.master.withdraw()
        self.SlaveWindow = tk.Toplevel(self.master)
        #self.ChildWindow.geometry('350x350')
        self.appStartQuiz = modStartQuiz_MCQ.ClassStartQuiz_MCQ(self.master,self.SlaveWindow)
#Ending Function**********************************************#
