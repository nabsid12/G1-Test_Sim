##    This file contains the class of a G1 Quiz test.
##    All MCQs records are categorized in two type. 1. Signs 2. Rules
##    There are 131 Signs MCQs and 120 Rules MCQs.
##    20 randomized MCQs of Signs will asked.
##    20 randomized MCQs of Rules will asked.
##    The program has ability to handle 2-5 options of answers.
##    But the data exported usually has 4 options and few 2 options of answers.
##    The program also always randomized the given options of answers.
##    In the program user can submit the answers to check the result.
##    The user can see the result for passing and failing.
##    For each question, answer is provided and where necessary explanations are given.

import tkinter as tk
from tkinter import messagebox
import os
import mysql.connector
import PIL
from PIL import ImageTk
import random
import uuid
import time

class ClassStartQuiz_MCQ:
    def __init__(self, master, slave):
        strDisplayText = "G1 Quiz"
        self.master = master
        self.slave = slave
        self.slave.geometry()
        #self.slave.resizable(0,0)
        self.slave.resizable(False, False)
        self.slave.title(strDisplayText) #Show title
        self.strWinTitle = strDisplayText
        self.MyFinalSignsResult=""
        self.MyFinalRulesResult=""
        self.listRecords2020 = []
        self.CurRecNum = 0
        self.isSubmitted = 0
        self.uniqeQuizID = None
        self.dictRecType = {"Signs":1, "Rules":2}
        self.dictRecNoOfQs = {"Signs":20, "Rules":20}
        self.dbConnWDB = None
        self.dbConnWDBCursor = None
        self.dbCnHost = self.master.conHost #host='127.0.0.1'
        self.dbCnUser = self.master.conUser
        self.dbCnPassword = self.master.conPassword
        self.strDbName = "dbMCQTest"
        self.strTbName_MCQ = "dbMCQTest.tbMCQTest"
        self.strTbName_Images = "dbMCQTest.tbImages"
        self.strTbName_QuizDetails = "dbMCQTest.tbQuizDetails"
        self.imageExitIcon = None
        self.imageStartIcon = None
        self.imageNextIcon = None
        self.imagePreviousIcon = None
        self.imageCarIcon = None
        self.imageMouse = None
        self.imageSurprisedPng = None
        self.imageSubmitIcon = None
        self.imimageCorrectPng = None
        self.imageWrongPng = None
        self.btn1_Previous = None
        self.btn1_Next = None
        self.btn1_Start = None
        self.btn1_Submit = None
        self.btn1_Exit = None        
        self.frameParentTop = tk.Frame(self.slave,width=100,height=80)
        #self.frameParentTop.configure(width=100,height=80)
        self.frameParentTop.grid(column=0, row=0, sticky=tk.W)     
        #Frames Creating of ParentQuestion and its children******************************************************
        self.frameParentQuizQ = tk.Frame(self.frameParentTop,width=200,height=80,highlightthickness=2,relief='raised')
        self.frameParentQuizQ.grid(column=0, row=0, sticky=tk.W)
        self.frameChildQuizQ = []
        for intChildCounter in range(7):
            self.frameChildQuizQ.append(tk.Frame(self.frameParentQuizQ,width=200,height=10,padx=1,pady=1))
            self.frameChildQuizQ[intChildCounter].grid(column=0, row=intChildCounter, sticky=tk.W)
        self.labelTextQ = tk.StringVar()
        self.label_Q = tk.Label(self.frameChildQuizQ[0], font=('arial',14,'bold'), foreground="red", text="", textvariable=self.labelTextQ, wraplength=500,justify="left")
        self.label_Q.grid(column=0, row=0, sticky=tk.W)
        self.label_Image1 = tk.Label(self.frameChildQuizQ[1])
        self.label_Image1.grid(column=0, row=1, sticky=tk.W)
        self.chkTextOpt = []
        self.chkIntValOpt = []
        self.checkBtnOpt = []
        for intChkBtn in range(5):
            self.chkTextOpt.append(tk.StringVar())
            self.chkIntValOpt.append(tk.IntVar())
            self.checkBtnOpt.append(tk.Checkbutton(self.frameChildQuizQ[intChkBtn+2], font=('arial',12,'bold'), foreground="blue", text="A.", textvariable=self.chkTextOpt[intChkBtn], variable=self.chkIntValOpt[intChkBtn], wraplength=500,justify="left"))
            self.checkBtnOpt[intChkBtn].grid(row=0, column=1, sticky=tk.W)
##        self.frameStatus = tk.Frame(self.slave,width=20,height=10,highlightbackground="blue",highlightthickness=2,relief='raised')
##        self.frameStatus.grid(column=0, row=1, sticky=tk.W)
##        self.frameParentBottom = tk.Frame(self.slave,width=20,height=10)
##        self.frameParentBottom.grid(column=0, row=2, sticky=tk.W)
##        self.frameNavigation = tk.Frame(self.frameParentBottom,width=20,height=10,padx=1,pady=1,highlightbackground="blue",highlightthickness=2,relief='raised')
##        self.frameNavigation.grid(column=0, row=0, sticky=tk.W)
##        self.frameStartSubmitProgramme = tk.Frame(self.frameParentBottom,width=20,height=10,padx=1,pady=1,highlightbackground="blue",highlightthickness=2,relief='raised')
##        self.frameStartSubmitProgramme.grid(column=1, row=0, sticky=tk.W)
##        self.frameExit = tk.Frame(self.frameParentBottom,width=20,height=10,padx=1,pady=1,highlightbackground="blue",highlightthickness=2,relief='raised')
##        self.frameExit.grid(column=2, row=0, sticky=tk.W)
        self.fn_DBConWithDB() #Call function for connection
        self.fn_getImages() #Call function for Getting Images
        self.slave.iconphoto(self, self.imageCarIcon) #Call function for Window Title
        #self.fn_createButtons()
        self.frameAnswerStatusInfo = tk.Frame(self.slave,width=200,height=10)
        self.frameAnswerStatusInfo.grid(column=0, row=1, sticky=tk.W)
        self.label1_AnswerStatusImage = tk.Label(self.frameAnswerStatusInfo)
        self.label1_AnswerStatusImage.configure(image=None)
        #self.label1_AnswerStatusImage.configure(image=self.imageStartPng)
        #self.label1_AnswerStatusImage.image=self.imageStartPng
        self.label1_AnswerStatusImage.grid(column=0, row=0, sticky=tk.W)
        self.label1_AnswerStatusDescription = tk.Label(self.frameAnswerStatusInfo,text="",font=('arial',8,'bold'),wraplength=500,justify="left")
        self.label1_AnswerStatusDescription.grid(column=1, row=0, sticky=tk.W)
        self.label1_ResultSignsRules = tk.Label(self.frameAnswerStatusInfo,text="",font=('arial',12,'bold'),fg="blue",wraplength=500,justify="left")
        self.label1_ResultSignsRules.grid(row=1, columnspan=2),
        self.frameStartInfo = tk.Frame(self.slave,width=200,height=10)
        self.frameStartInfo.grid(column=0, row=2, sticky=tk.W)
        #***Starting*******Quiz Clock
        self.strVar_QuizClock = tk.StringVar()
        self.btn_QuizClock = tk.Button(self.frameStartInfo, fg="blue", compound=tk.BOTTOM, font=('arial',18,'bold'), state=tk.DISABLED,textvariable=self.strVar_QuizClock, command=lambda:self.fn_Update_StatusClock(self.strVar_QuizClock))
        self.btn_QuizClock.grid(column=0, row=0, sticky=tk.W)
        self.fn_Update_StatusClock(self.strVar_QuizClock)
        #***Ending*********Quiz Clock
        #***Starting*******Quiz Timer
        self.timeQuizTimeLimit = 30
        self.strVar_QuizTimer = tk.StringVar()
        self.btn_QuizTimer = tk.Button(self.frameStartInfo, fg="blue", compound=tk.BOTTOM, font=('arial',18,'bold'), state=tk.DISABLED,textvariable=self.strVar_QuizTimer, command=lambda:self.fn_submitQuizMCQ("Initial"))
        self.btn_QuizTimer.grid(column=1, row=0, sticky=tk.W)
        #***Ending*********Quiz Timer
        self.label1_StartInfoImage = tk.Label(self.frameStartInfo)
        self.label1_StartInfoImage.configure(image=self.imageStartPng)
        self.label1_StartInfoImage.image=self.imageStartPng
        self.label1_StartInfoImage.grid(column=2, row=0, sticky=tk.W)
        self.label1_StartInfoText = tk.Label(self.frameStartInfo, font=('arial',10,'bold'), text='Please click "Start" button to start or restart the program.', fg="black",wraplength=500,justify="left")
        self.label1_StartInfoText.grid(column=3, row=0, sticky=tk.W)
        self.frameButtons = tk.Frame(self.slave,width=200,height=10)
        self.frameButtons.grid(column=0, row=3, sticky=tk.W)
        self.btn1_Previous = tk.Button(self.frameButtons, text="Previous", height=40, width=60, border=10, compound=tk.BOTTOM, command=lambda:self.fn_Navigate_Record("Previous"))
        self.btn1_Previous.configure(image=self.imagePreviousIcon)
        self.btn1_Previous.image=self.imagePreviousIcon
        self.btn1_Previous.grid(column=0, row=0, sticky=tk.W)
        self.btn1_Next = tk.Button(self.frameButtons, text="Next", height=40, width=60, border=10, compound=tk.BOTTOM, command=lambda:self.fn_Navigate_Record("Next"))
        self.btn1_Next.configure(image=self.imageNextIcon)
        self.btn1_Next.image=self.imageNextIcon 
        self.btn1_Next.grid(column=1, row=0, sticky=tk.W)
        self.btn1_Start = tk.Button(self.frameButtons, text="Start", height=40, width=60, border=10, compound=tk.BOTTOM, command=lambda:self.fn_startQuizMCQ())
        self.btn1_Start.configure(image=self.imageStartIcon)
        self.btn1_Start.image = self.imageStartIcon 
        self.btn1_Start.grid(column=2, row=0, sticky=tk.W)
        self.btn1_Submit = tk.Button(self.frameButtons, text="Submit", height=40, width=60, border=10, compound=tk.BOTTOM, command=lambda:self.fn_submitQuizMCQ("Submit Button"))
        self.btn1_Submit.configure(image = self.imageSubmitIcon)
        self.btn1_Submit.image = self.imageSubmitIcon 
        self.btn1_Submit.grid(column=3, row=0, sticky=tk.W)
        self.btn1_Exit = tk.Button(self.frameButtons, text="Exit", height=40, width=60, border=10, compound=tk.BOTTOM, command=lambda:self.fn_exitQuizMCQ())
        self.btn1_Exit.configure(image=self.imageExitIcon)
        self.btn1_Exit.image=self.imageExitIcon 
        self.btn1_Exit.grid(column=4, row=0, sticky=tk.W)
        #startup
        self.frameParentTop.configure(width=100,height=100)
        self.fn_fillMCQQuizTable()
        self.fn_fillMCQList()
        self.MyFinalSignsResult=""
        self.MyFinalRulesResult=""
        self.btn1_Submit.configure(state=tk.NORMAL)
        for intCounter in range(5):
            self.checkBtnOpt[intCounter].configure(state=tk.NORMAL)
        self.isSubmitted = 0
        strIsSubmitted = "notSubmitted"
        self.fn_Navigate_Record("Start")
        #***Starting*******Quiz Timer
        self.strVar_QuizTimer.set(self.timeQuizTimeLimit)
        self.fn_QuizCountDown(self.timeQuizTimeLimit,self.strVar_QuizTimer)
        #***Ending*********Quiz Timer
        
    def fn_DBConWithDB(self):
        try:
            self.dbConnWDB = mysql.connector.connect(
                host = self.dbCnHost, #host='127.0.0.1'
                user = self.dbCnUser,
                password = self.dbCnPassword,
                database = self.strDbName
                )
            self.dbConnWDBCursor = self.dbConnWDB.cursor()
            return 1
        except Exception as e:
            messagebox.showinfo(self.strWinTitle, 'Exception occured in the database connection! {}'.format(e))
            return -1

    def fn_getImages(self):
        strImagesNamesList = "('car-icon', 'previous-icon', 'next-icon', 'start-icon', 'submit-icon', 'exit-icon', 'start-png', 'surprised-png', 'correct-png', 'wrong-png', 'pass-png', 'fail-png') ORDER BY Image_FileName"
        self.dbConnWDBCursor.execute("SELECT Image_FileName, Image_Data FROM " + self.strTbName_Images + " WHERE Image_RecActive = 1 AND Image_FileName IN " + strImagesNamesList)
        myResultImages = self.dbConnWDBCursor.fetchall()
        for xImageQuiz in myResultImages:
            if xImageQuiz[0].upper()=='car-icon'.upper():
               self.imageCarIcon = PIL.ImageTk.PhotoImage(data=xImageQuiz[1])
            if xImageQuiz[0].upper()=='previous-icon'.upper():
                self.imagePreviousIcon = PIL.ImageTk.PhotoImage(data=xImageQuiz[1])
            if xImageQuiz[0].upper()=='next-icon'.upper():
                self.imageNextIcon = PIL.ImageTk.PhotoImage(data=xImageQuiz[1])
            if xImageQuiz[0].upper()=='start-icon'.upper():
                self.imageStartIcon = PIL.ImageTk.PhotoImage(data=xImageQuiz[1])
            if xImageQuiz[0].upper()=='submit-icon'.upper():
                self.imageSubmitIcon = PIL.ImageTk.PhotoImage(data=xImageQuiz[1])
            if xImageQuiz[0].upper()=='exit-icon'.upper():
                self.imageExitIcon = PIL.ImageTk.PhotoImage(data=xImageQuiz[1])
            if xImageQuiz[0].upper()=='start-png'.upper():
                self.imageStartPng = PIL.ImageTk.PhotoImage(data=xImageQuiz[1])
            if xImageQuiz[0].upper()=='surprised-png'.upper():
                self.imageSurprisedPng = PIL.ImageTk.PhotoImage(data=xImageQuiz[1])
            if xImageQuiz[0].upper()=='correct-png'.upper():
                self.imageCorrectPng = PIL.ImageTk.PhotoImage(data=xImageQuiz[1])
            if xImageQuiz[0].upper()=='wrong-png'.upper():
                self.imageWrongPng = PIL.ImageTk.PhotoImage(data=xImageQuiz[1])
            if xImageQuiz[0].upper()=='pass-png'.upper():
                self.imagePassPng = PIL.ImageTk.PhotoImage(data=xImageQuiz[1])
            if xImageQuiz[0].upper()=='fail-png'.upper():
                self.imageFailPng = PIL.ImageTk.PhotoImage(data=xImageQuiz[1])

    def fn_startQuizMCQ(self):
        messageBox1 = messagebox.askyesno(self.strWinTitle, 'Are you sure to start test?')
        if messageBox1 == True:
            self.frameParentTop.configure(width=100,height=100)
            self.fn_fillMCQQuizTable()
            self.fn_fillMCQList()
            self.MyFinalSignsResult=""
            self.MyFinalRulesResult=""
            self.btn1_Submit.configure(state=tk.NORMAL)
            for intCounter in range(5):
                self.checkBtnOpt[intCounter].configure(state=tk.NORMAL)
            self.isSubmitted = 0
            strIsSubmitted = "notSubmitted"
            self.fn_Navigate_Record("Start")
            #***Starting*******Quiz Timer
            self.strVar_QuizTimer.set(self.timeQuizTimeLimit)
            self.fn_QuizCountDown(self.timeQuizTimeLimit,self.strVar_QuizTimer)
            #***Ending*********Quiz Timer
            
    def fn_submitQuizMCQ(self, para_source):
        #global strIsSubmitted
        if para_source=="Submit Button":
            messageBox1 = messagebox.askyesno(self.strWinTitle, 'Are you sure to submit answers?')
            if messageBox1 == False:
                return
        self.btn1_Submit.configure(state=tk.DISABLED)
        for intCounter in range(5):
            self.checkBtnOpt[intCounter].configure(state=tk.DISABLED)
        self.isSubmitted = 1
        strIsSubmitted = "notSubmitted"
        self.fn_Navigate_Record("Submit")
        if self.isSubmitted == 1:
            intMyFinalSignsResult=0
            for intAnsCounter in range(20):
                if self.listRecords2020[intAnsCounter][26]==1:
                    intMyFinalSignsResult+=1
            intMyFinalRulesResult=0
            for intAnsCounter in range(20,40):
                if self.listRecords2020[intAnsCounter][26]==1:
                    intMyFinalRulesResult+=1
            if intMyFinalSignsResult>15:
                self.MyFinalSignsResult = "Signs Score: " + str(intMyFinalSignsResult) + "/20 - Pass"
            else:
                self.MyFinalSignsResult = "Signs Score: " + str(intMyFinalSignsResult) + "/20 - Fail"
            if intMyFinalRulesResult>15:
                self.MyFinalRulesResult = "Rules Score: " + str(intMyFinalRulesResult) + "/20 - Pass"
            else:
                self.MyFinalRulesResult = "Rules Score: " + str(intMyFinalRulesResult) + "/20 - Fail"
            if self.listRecords2020[self.CurRecNum-1][26]==1:
                self.label1_AnswerStatusImage.configure(image=self.imageCorrectPng)
                self.label1_AnswerStatusImage.image=self.imageCorrectPng
            else:
                self.label1_AnswerStatusImage.configure(image=self.imageWrongPng)
                self.label1_AnswerStatusImage.image=self.imageWrongPng
            strAnswerOfQ = "Correct Answer: "
            if self.listRecords2020[self.CurRecNum-1][16]==1:
                strAnswerOfQ += "A. "
            if self.listRecords2020[self.CurRecNum-1][18]==1:
                strAnswerOfQ += "B. "
            if self.listRecords2020[self.CurRecNum-1][20]==1:
                strAnswerOfQ += "C. "
            if self.listRecords2020[self.CurRecNum-1][22]==1:
                strAnswerOfQ += "D. "
            if self.listRecords2020[self.CurRecNum-1][24]==1:
                strAnswerOfQ += "E. "                    
            self.label1_AnswerStatusDescription.configure(text=strAnswerOfQ+self.listRecords2020[self.CurRecNum-1][27])
            self.label1_ResultSignsRules.configure(text=self.MyFinalSignsResult + "===" + self.MyFinalRulesResult)
            self.label1_AnswerStatusImage.grid()
            self.label1_AnswerStatusDescription.grid()
            self.label1_ResultSignsRules.grid()

    #Starting Clock***************************************************************************************************
    def fn_Update_StatusClock(self,para_btn_string):
        para_btn_string.set(time.strftime('%H:%M:%S %p',time.localtime()))
        #self.label1_StatusClock.config(text=time.strftime('%H:%M:%S %p',time.localtime()))
        # change the text of the time_label according to the current time
        self.slave.after(100,lambda:self.fn_Update_StatusClock(para_btn_string))  # reschedule update_clock function to update time_label every 100 ms
    #Ending Clock*****************************************************************************************************

    def fn_QuizCountDown(self,para_quizTimeLimit,para_btn_string):
        if para_quizTimeLimit > 0:
            para_quizTimeLimit -= 1
            #para_btn_string.set(para_quizTimeLimit)
            para_btn_string.set(str(int(int((para_quizTimeLimit/60)-1)/60)).zfill(2)+ ":"+str(int((para_quizTimeLimit%3600-1)/60)).zfill(2)+ ":"+str(para_quizTimeLimit%60).zfill(2))
            self.slave.after(1000,lambda:self.fn_QuizCountDown(para_quizTimeLimit,para_btn_string))
        else:
            self.fn_submitQuizMCQ("Timer")
        
    def fn_exitQuizMCQ(self):
        messageBox1 = messagebox.askyesno(self.strWinTitle, "Are you sure to exit?")
        if messageBox1 == True:
            os._exit(0)

    def fn_fillMCQQuizTable_RecType(self,para_MCQRecType,para_MCQRecNoOfQs,para_MCQRecStartAfter):
        strSQL1 = ("SELECT MCQ_ID FROM " + self.strTbName_MCQ + " WHERE MCQ_RecActive=1 "
                   "AND MCQ_RecType = " + str(para_MCQRecType)) #Get all RecID with particular record type
        self.dbConnWDBCursor.execute(strSQL1)
        myTupleResult = self.dbConnWDBCursor.fetchall() #Store all RecID as tuple in a list
        myTupleResultRandom20 = random.sample(myTupleResult, k = para_MCQRecNoOfQs) #Get 20 random RecID
        myList20 = [] #Declare list
        for recID in myTupleResultRandom20: #Changing tuple to list
            myList20.append(recID[0])
        for intSeqNo in range(20): #Get record from MCQTable and insert into QuizTable
            strSQL2 = "SELECT MCQ_TotalOptions FROM " + self.strTbName_MCQ + " WHERE MCQ_ID = " + str(myList20[intSeqNo])
            self.dbConnWDBCursor.execute(strSQL2)
            myMCQRow = self.dbConnWDBCursor.fetchall() #Get number of options and randomize the options
            myListOpt = []
            if myMCQRow[0][0]==2:
               myListOpt = random.sample(["1","2"], k = 2)
               myListOpt.extend(["3","4","5"])
            elif myMCQRow[0][0]==3:
               myListOpt = random.sample(["1","2","3"], k = 3)
               myListOpt.extend(["4","5"])
            elif myMCQRow[0][0]==4:
               myListOpt = random.sample(["1","2","3","4"], k = 4)
               myListOpt.extend(["5"])
            elif myMCQRow[0][0]==5:
               myListOpt = random.sample(["1","2","3","4","5"], k = 5)
            strSQL3_a = ("INSERT INTO " + self.strTbName_QuizDetails + " (Quiz_RecActive, Quiz_UUID, QuizMaster_ID, Quiz_SNo, MCQ_ID, "
                "Quiz_RecType, Quiz_QText, Quiz_Image1, Quiz_Image2, Quiz_TotalOptions, "
                "Quiz_OptText1, Quiz_OptText2, Quiz_OptText3, "
                "Quiz_OptText4, Quiz_OptText5, "
                "Quiz_AOpt1, Quiz_AOpt2, Quiz_AOpt3, "
                "Quiz_AOpt4, Quiz_AOpt5, "
                "Quiz_AnsExpDes) ")
            strSQL3_b = ("SELECT MCQ_RecActive, '" + self.uniqeQuizID + "', NULL, " + str(para_MCQRecStartAfter+intSeqNo+1) + ", "
                "MCQ_ID, MCQ_RecType, MCQ_QText, MCQ_Image1, MCQ_Image2, MCQ_TotalOptions, "
                "MCQ_OptText" + myListOpt[0] + ", MCQ_OptText" + myListOpt[1] + ", MCQ_OptText" + myListOpt[2] + ", "
                "MCQ_OptText" + myListOpt[3] + ", MCQ_OptText" + myListOpt[4] + ", MCQ_AOpt" + myListOpt[0] + ", "
                "MCQ_AOpt" + myListOpt[1] + ", MCQ_AOpt" + myListOpt[2] + ", MCQ_AOpt" + myListOpt[3] + ", "
                "MCQ_AOpt" + myListOpt[4] + ", MCQ_AnsExpDes FROM " + self.strTbName_MCQ + " WHERE MCQ_ID"
                " = " + str(myList20[intSeqNo]))
            strSQL3 = strSQL3_a + strSQL3_b
            self.dbConnWDBCursor.execute(strSQL3)
            self.dbConnWDB.commit()
            strSQL4 = ("UPDATE " + self.strTbName_QuizDetails + " SET Quiz_UOpt1=0, Quiz_UOpt2=0, Quiz_UOpt3=0, Quiz_UOpt4=0, "
                "Quiz_UOpt5=0, Quiz_AnsNum=0 WHERE Quiz_UUID = '" + self.uniqeQuizID + "'")
            self.dbConnWDBCursor.execute(strSQL4)
            self.dbConnWDB.commit()
                       
    def fn_fillMCQQuizTable(self):
        self.uniqeQuizID = str(uuid.uuid4()) #Generate Unique ID
        self.fn_fillMCQQuizTable_RecType(self.dictRecType["Signs"],self.dictRecNoOfQs["Signs"],0)
        self.fn_fillMCQQuizTable_RecType(self.dictRecType["Rules"],self.dictRecNoOfQs["Rules"],self.dictRecNoOfQs["Signs"])

    def fn_fillMCQList(self):
        strSQL1 = ("SELECT QuizDetails_ID, Quiz_RecActive, Quiz_UUID, QuizMaster_ID, Quiz_SNo, MCQ_ID, Quiz_RecType, Quiz_QText, "
            "Quiz_Image1, Quiz_Image2, Quiz_TotalOptions, Quiz_OptText1, Quiz_OptText2, Quiz_OptText3, Quiz_OptText4, "
            "Quiz_OptText5, Quiz_AOpt1, Quiz_UOpt1, Quiz_AOpt2, Quiz_UOpt2, Quiz_AOpt3, Quiz_UOpt3, Quiz_AOpt4, Quiz_UOpt4, "
            "Quiz_AOpt5, Quiz_UOpt5, Quiz_AnsNum, Quiz_AnsExpDes FROM " + self.strTbName_QuizDetails + " WHERE Quiz_UUID = "
            "'" + self.uniqeQuizID + "' ORDER BY Quiz_RecType,Quiz_SNo")
            #"'2affc324-30f2-48fb-a162-e38ccfc0c828' ORDER BY Quiz_RecType,Quiz_SNo")
        self.dbConnWDBCursor.execute(strSQL1)
        myTupleListResult = self.dbConnWDBCursor.fetchall()
        myListRndRecords = []
        for listRec in myTupleListResult:
            myListRndRecords.append(list(listRec))
        self.listRecords2020.clear()
        self.listRecords2020 = list(myListRndRecords)
        #print(len(self.listRecords2020))

    def fn_Navigate_Record(self,para_ClickNavBtn):
        if para_ClickNavBtn=="Start":
            self.CurRecNum = 1
            self.fn_DisplayRecord(self.CurRecNum)
        elif para_ClickNavBtn=="Previous":
            if self.CurRecNum == 1:
                messagebox.showinfo(self.strWinTitle, "This is the first record and cannot show the previous record!")
            elif self.CurRecNum == 2:
                self.fn_SaveRecord(self.CurRecNum)
                self.CurRecNum = 1
                self.fn_DisplayRecord(self.CurRecNum)
                messagebox.showinfo(self.strWinTitle, "This is the first record!")
            else:
                self.fn_SaveRecord(self.CurRecNum)
                self.CurRecNum -= 1
                self.fn_DisplayRecord(self.CurRecNum)
        elif para_ClickNavBtn=="Next":
            if self.CurRecNum == 40:
                messagebox.showinfo(self.strWinTitle, "This is the last record and cannot show the next record!")
            elif self.CurRecNum == 39:
                self.fn_SaveRecord(self.CurRecNum)
                self.CurRecNum = 40
                self.fn_DisplayRecord(self.CurRecNum)
                messagebox.showinfo(self.strWinTitle, "This is the last record!")
            else:
                self.fn_SaveRecord(self.CurRecNum)
                self.CurRecNum += 1
                self.fn_DisplayRecord(self.CurRecNum)
        elif para_ClickNavBtn=="Submit":
            self.fn_SaveRecord(self.CurRecNum)
            
    def fn_SaveRecord(self,para_RecNum):
        if self.chkIntValOpt[0].get() is None:
            self.listRecords2020[self.CurRecNum-1][17] = 0
        elif self.chkIntValOpt[0].get()==0:
            self.listRecords2020[self.CurRecNum-1][17] = 0
        else:
            self.listRecords2020[self.CurRecNum-1][17] = 1
        if self.chkIntValOpt[1].get() is None:
            self.listRecords2020[self.CurRecNum-1][19] = 0
        elif self.chkIntValOpt[1].get()==0:
            self.listRecords2020[self.CurRecNum-1][19] = 0
        else:
            self.listRecords2020[self.CurRecNum-1][19] = 1
        if self.chkIntValOpt[2].get() is None:
            self.listRecords2020[self.CurRecNum-1][21] = 0
        elif self.chkIntValOpt[2].get()==0:
            self.listRecords2020[self.CurRecNum-1][21] = 0
        else:
            self.listRecords2020[self.CurRecNum-1][21] = 1
        if self.chkIntValOpt[3].get() is None:
            self.listRecords2020[self.CurRecNum-1][23] = 0
        elif self.chkIntValOpt[3].get()==0:
            self.listRecords2020[self.CurRecNum-1][23] = 0
        else:
            self.listRecords2020[self.CurRecNum-1][23] = 1
        if self.chkIntValOpt[4].get() is None:
            self.listRecords2020[self.CurRecNum-1][25] = 0
        elif self.chkIntValOpt[4].get()==0:
            self.listRecords2020[self.CurRecNum-1][25] = 0
        else:
            self.listRecords2020[self.CurRecNum-1][25] = 1
        if self.listRecords2020[self.CurRecNum-1][16]==1 and self.listRecords2020[self.CurRecNum-1][17]==1:
            self.listRecords2020[self.CurRecNum-1][26] = 1
        if self.listRecords2020[self.CurRecNum-1][18]==1 and self.listRecords2020[self.CurRecNum-1][19]==1:
            self.listRecords2020[self.CurRecNum-1][26] = 1
        if self.listRecords2020[self.CurRecNum-1][20]==1 and self.listRecords2020[self.CurRecNum-1][21]==1:
            self.listRecords2020[self.CurRecNum-1][26] = 1
        if self.listRecords2020[self.CurRecNum-1][22]==1 and self.listRecords2020[self.CurRecNum-1][23]==1:
            self.listRecords2020[self.CurRecNum-1][26] = 1
        if self.listRecords2020[self.CurRecNum-1][24]==1 and self.listRecords2020[self.CurRecNum-1][25]==1:
            self.listRecords2020[self.CurRecNum-1][26] = 1
        
    def fn_DisplayRecord(self,para_RecNum):
        self.labelTextQ.set("Q" + (str(self.CurRecNum)).zfill(2)+ ". " + self.listRecords2020[self.CurRecNum-1][7])
        image1 = PIL.ImageTk.PhotoImage(data=self.listRecords2020[self.CurRecNum-1][8])
        self.label_Image1.configure(image=image1)
        self.label_Image1.image = image1        
        self.chkTextOpt[0].set("A. " + self.listRecords2020[self.CurRecNum-1][11])
        self.chkIntValOpt[0].set(self.listRecords2020[self.CurRecNum-1][17])
        self.chkTextOpt[1].set("B. " + self.listRecords2020[self.CurRecNum-1][12])
        self.chkIntValOpt[1].set(self.listRecords2020[self.CurRecNum-1][19])
        if self.listRecords2020[self.CurRecNum-1][10]>2 and self.listRecords2020[self.CurRecNum-1][13] is not None:
            self.chkTextOpt[2].set("C. " + self.listRecords2020[self.CurRecNum-1][13])
            self.checkBtnOpt[2].grid()
            self.chkIntValOpt[2].set(self.listRecords2020[self.CurRecNum-1][21])
        else:
            self.checkBtnOpt[2].grid_remove()
        if self.listRecords2020[self.CurRecNum-1][10]>3 and self.listRecords2020[self.CurRecNum-1][14] is not None:
            self.chkTextOpt[3].set("D. " + self.listRecords2020[self.CurRecNum-1][14])
            self.checkBtnOpt[3].grid()
            self.chkIntValOpt[3].set(self.listRecords2020[self.CurRecNum-1][23])
        else:
            self.checkBtnOpt[3].grid_remove()        
        if self.listRecords2020[self.CurRecNum-1][10]==5 and self.listRecords2020[self.CurRecNum-1][15] is not None:
            self.chkTextOpt[4].set("E. " + self.listRecords2020[self.CurRecNum-1][15])
            self.checkBtnOpt[4].grid()
            self.chkIntValOpt[4].set(self.listRecords2020[self.CurRecNum-1][25])
        else:
            self.checkBtnOpt[4].grid_remove()
        if self.isSubmitted == 1:
            if self.listRecords2020[self.CurRecNum-1][26]==1:
                self.label1_AnswerStatusImage.configure(image=self.imageCorrectPng)
                self.label1_AnswerStatusImage.image=self.imageCorrectPng
            else:
                self.label1_AnswerStatusImage.configure(image=self.imageWrongPng)
                self.label1_AnswerStatusImage.image=self.imageWrongPng
            strAnswerOfQ = "Correct Answer: "
            if self.listRecords2020[self.CurRecNum-1][16]==1:
                strAnswerOfQ += "A. "
            if self.listRecords2020[self.CurRecNum-1][18]==1:
                strAnswerOfQ += "B. "
            if self.listRecords2020[self.CurRecNum-1][20]==1:
                strAnswerOfQ += "C. "
            if self.listRecords2020[self.CurRecNum-1][22]==1:
                strAnswerOfQ += "D. "
            if self.listRecords2020[self.CurRecNum-1][24]==1:
                strAnswerOfQ += "E. "
            self.label1_AnswerStatusDescription.configure(text=strAnswerOfQ+self.listRecords2020[self.CurRecNum-1][27])
            self.label1_ResultSignsRules.configure(text=self.MyFinalSignsResult + "===" + self.MyFinalRulesResult)
            self.label1_AnswerStatusImage.grid()
            self.label1_AnswerStatusDescription.grid()
            self.label1_ResultSignsRules.grid()
        else:
            self.label1_AnswerStatusImage.configure(image=None)
            self.label1_AnswerStatusImage.image=None
            self.label1_AnswerStatusImage.grid_remove()
            self.label1_AnswerStatusDescription.configure(text=None)
            self.label1_AnswerStatusDescription.grid_remove()
            self.label1_ResultSignsRules.grid_remove()
