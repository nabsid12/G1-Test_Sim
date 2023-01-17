# This file contains the class of exporting G1 Signs and Rules MCQs text and images info to a table.

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
import mysql.connector

class ClassExportData_MCQ:
    def __init__(self, master, slave, para_MCQType):
        self.master = master
        self.slave = slave
        self.MCQType = para_MCQType
        self.slave.geometry()
        strMCQType = ""
        self.slave.resizable(0,0)
        if self.MCQType==1:
            strMCQType = "Signs"
        elif self.MCQType==2:
            strMCQType = "Rules"
        self.slave.title("G1 Test - Export - " + strMCQType + " Data") #Show title
        self.strWinTitle = "G1 Test - Export - " + strMCQType + " Data"
        self.dbConnWODB = None
        self.dbConnWODBCursor = None
        self.dbConnWDB = None
        self.dbConnWDBCursor = None
        self.dbCnHost = self.master.conHost
        self.dbCnUser = self.master.conUser
        self.dbCnPassword = self.master.conPassword
        self.strDbName = "dbMCQTest"
        self.strTbName_MCQ = "dbMCQTest.tbMCQTest"
        self.strTbName_MCQOnly = "tbMCQTest"
        self.strSQL_FindDB = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '" + self.strDbName.upper() + "'"
        self.strSQL_FindTB_MCQ = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA = '" + self.strDbName.upper() + "' AND TABLE_NAME = '" + self.strTbName_MCQOnly.upper() + "'"
        self.strSQL_ITB = "INSERT INTO " + self.strTbName_MCQ + " (MCQ_RecActive, MCQ_RecType, MCQ_QText, MCQ_Image1, MCQ_Image2, MCQ_TotalOptions, MCQ_OptText1, MCQ_OptText2, MCQ_OptText3, MCQ_OptText4, MCQ_OptText5, MCQ_AOpt1, MCQ_UOpt1, MCQ_AOpt2, MCQ_UOpt2, MCQ_AOpt3, MCQ_UOpt3, MCQ_AOpt4, MCQ_UOpt4, MCQ_AOpt5, MCQ_UOpt5, MCQ_AnsNum, MCQ_AnsExpDes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.strStatusDB = "NotExistDatabase"
        self.strStatusTB_MCQ = "NotExistTable_MCQ"
        
        dataFrame = []
        lblList = []
        lblListString = ["Text File Name Path","Images Folder Path"]
        entListString = ["",""]
        self.entList = []
        self.entTextInput = []
        btnList = []
        btnListString = ["Exit","Export"]

#Starting*********************************************#
        dataFrameHeader = tk.Frame(slave)
        dataFrameHeader.grid(row=0)
        lblHeader = tk.Label(dataFrameHeader, text = self.strWinTitle, font=('arial',24,'bold'),
                             width=42,padx=2,pady=12,bd=8,fg="Cornsilk", bg='cadet blue',)
        lblHeader.grid(row=0,column=0)
#Ending***********************************************#
#Starting*********************************************#
        dataFrame.append(tk.Frame(slave))
        dataFrame[0].grid(row=1,columnspan=3)
        lblList.append(tk.Label(dataFrame[0], text = lblListString[0], font=('arial',12,'bold'),
                             width=15,padx=8,pady=16,bd=8,fg="blue", bg='powder blue',))
        lblList[0].grid(row=1,column=0)
        btnTF = tk.Button(dataFrame[0],text = "...", font=('arial',10,'bold'),
                              width=3,padx=4,pady=8,bd=16,fg="blue", bg='powder blue',
                              command=lambda:self.fn_TextFileLocation(self.MCQType))
        btnTF.grid(row=1,column=1)
        
        self.entTextInput.append(tk.StringVar())
        self.entTextInput[0].set(entListString[0])
        self.entList.append(tk.Entry(dataFrame[0], textvariable=self.entTextInput[0], justify='left', font=('arial',12,'bold'),
                            width=60, bd=20, insertwidth=8, bg='white', state='disabled',))
        self.entList[0].grid(row=1,column=2)
#Ending***********************************************#
#Starting*********************************************#
        dataFrame.append(tk.Frame(slave))
        dataFrame[1].grid(row=2,columnspan=3)
        lblList.append(tk.Label(dataFrame[1], text = lblListString[1], font=('arial',12,'bold'),
                             width=15,padx=8,pady=16,bd=8,fg="blue", bg='powder blue',))
        lblList[1].grid(row=2,column=0)
        btnIF = tk.Button(dataFrame[1],text = "...", font=('arial',10,'bold'),
                              width=3,padx=4,pady=8,bd=16,fg="blue", bg='powder blue',
                              command=lambda:self.fn_ImageFolderLocation(self.MCQType))
        btnIF.grid(row=2,column=1)        
        self.entTextInput.append(tk.StringVar())
        self.entTextInput[1].set(entListString[1])
        self.entList.append(tk.Entry(dataFrame[1], textvariable=self.entTextInput[1], justify='left', font=('arial',12,'bold'),
                            width=60, bd=20, insertwidth=8, bg='white', state='disabled',))
        self.entList[1].grid(row=2,column=2)
#Ending***********************************************#
#Starting*********************************************#
##        dataFrame.append(tk.Frame(slave))
##        dataFrame[2].grid(row=3,columnspan=1)
##        self.cboDataType = ttk.TCombobox(dataFrame[2],values=["Signs Text Data File and Images","Rules Text Data File and Images"])
##        self.cboDataType.grid(row=2,column=3)
#Ending***********************************************#        
#Starting*********************************************#
        dataFrame.append(tk.Frame(slave))
        dataFrame[2].grid(row=3,columnspan=2)
        btnList.append(tk.Button(dataFrame[2],text = btnListString[0], font=('arial',16,'bold'),
                              width=6,padx=4,pady=8,bd=16,fg="blue", bg='powder blue',))
        btnList[0].grid(row=3,column=0)
        lblSpacer = tk.Label(dataFrame[2], text = "             ",width=6,padx=8,pady=16,bd=8,bg='powder blue',)
        lblSpacer.grid(row=3,column=1)
        btnList.append(tk.Button(dataFrame[2],text = btnListString[1], font=('arial',16,'bold'),
                              width=6,padx=4,pady=8,bd=16,fg="blue", bg='powder blue',))
        btnList[1].grid(row=3,column=2)
#Ending***********************************************#
        btnList[0].config(fg="red",bg='gold')
        list(map(lambda intVal: btnList[btnListString.index(intVal)].config(command=lambda:self.btnClicked(intVal)), btnListString))
        #btnList[0].focus()
        self.fn_CheckTB_MCQ()

    def fn_LeaveAfterExport(self):
        try:
            messagebox.showinfo(self.strWinTitle,'Text File Data and Images in the Folder has been exported successfully!')
            self.slave.destroy()
            self.master.update()
            self.master.deiconify()            
        except Exception as e:
            messagebox.showinfo(self.strWinTitle,'Exception occured! Please check Text File Data and Images in the Folder!')

    def fn_TextFileLocation(self,paraRecordType):
        if self.fn_CheckTB_MCQ()==False:
            return
        if paraRecordType==1:
            strRecType=" - Text File for Signs MCQs"
        else:
            strRecType=" - Text File for Rules MCQs"
        fileTextPath = filedialog.askopenfilename(title=self.strWinTitle+strRecType,multiple=False,initialdir="/",filetypes =(("Text Files","*.txt"),("Text Files","*.txt")))
        if str(fileTextPath)!="":
            self.entTextInput[0].set(str(fileTextPath))
        else:
            self.entTextInput[0].set("")
        #return strTextFileName

    def fn_ImageFolderLocation(self,paraRecordType):
        if self.fn_CheckTB_MCQ()==False:
            return        
        if paraRecordType==1:
            strRecType=" - Folder for Signs Images"
        else:
            strRecType=" - Folder for Rules Images"
        folderImagePath = filedialog.askdirectory(title=self.strWinTitle+strRecType,initialdir="/")
        if str(folderImagePath)!="":
            self.entTextInput[1].set(str(folderImagePath))
        else:
            self.entTextInput[1].set("")
        #return strImageFolderName
    
    def btnClicked(self,paraBtn):
        try:
            if paraBtn=="Export":
                if self.fn_CheckTB_MCQ()==False:
                    return
                if self.entTextInput[0].get()=="":
                    messagebox.showinfo(self.strWinTitle,'Please select Text File Data to export!')
                    return
                if self.entTextInput[1].get()=="":
                    messagebox.showinfo(self.strWinTitle,'Please select Folder of the Images Files!')
                    return
                if self.MCQType==1 or self.MCQType==2:
                    self.fn_DataInsertTable(self.MCQType)
            elif paraBtn=="Exit":
                msgBoxQ = messagebox.askquestion(self.strWinTitle + ' - Exit','Are you sure you want to exit Exporting of Text File Data and Images in the Folder window?',icon = 'warning')
                if msgBoxQ == 'yes':
                    self.slave.destroy()
                    self.master.update()
                    self.master.deiconify()
        except:
            messagebox.showinfo(self.strWinTitle,'Exception occured! {}'.format(e))

    def fn_setHostUserPassword(self,paraHost,paraUser,paraPassword):
        self.dbCnHost = paraHost
        self.dbCnUser = paraUser
        self.dbCnPassword = paraPassword
        
    def fn_DBConWithoutDB(self):
        try:
            self.dbConnWODB = mysql.connector.connect(
                host = self.dbCnHost,
                user = self.dbCnUser,
                password = self.dbCnPassword
                )
            self.dbConnWODBCursor = self.dbConnWODB.cursor()
            return 1
        except Exception as e:
            messagebox.showinfo(self.strWinTitle, 'Exception occured in MySQL connection! {}'.format(e))
            return -1
        
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
        
    def fn_CheckTB_MCQ(self):
        try:
            if self.dbConnWODB is None:
                self.fn_DBConWithoutDB()
            if self.dbConnWODB is not None:
                intDBExist = 0
                intTBExist = 0
                self.strStatusDB = "NotExistDatabase"
                self.strStatusTB_MCQ = "NotExistTable_MCQ"
                self.dbConnWODBCursor.execute(self.strSQL_FindDB)
                myResult = self.dbConnWODBCursor.fetchall()
                for forCursorDB in myResult:
                    intDBExist = forCursorDB[0]
                if intDBExist==0:
                    messagebox.showinfo(self.strWinTitle, 'Database "' + self.strDbName + '" has not been created! Nothing to export!')
                    return False
                else:
                    if self.dbConnWDB is None:
                        self.fn_DBConWithDB()
                    if self.dbConnWDB is not None:
                        self.dbConnWDBCursor.execute(self.strSQL_FindTB_MCQ)
                        myResult = self.dbConnWDBCursor.fetchall()
                        for forCursorTB in myResult:
                            intTBExist = forCursorTB[0]
                        if intTBExist==0:
                            messagebox.showinfo(self.strWinTitle, 'Table "' + self.strTbName_MCQOnly + '" has not been created! Nothing to export!')
                            return False
                        else:
                            return True
        except Exception as e:
            messagebox.showinfo(self.strWinTitle, 'Exception occured in dropping the table! {}'.format(e))

    def fn_DataCommitTable(self,paraListData):
        try:
            valInsert=(1,paraListData[0],paraListData[1],paraListData[2],paraListData[3],paraListData[4],
                       paraListData[5],paraListData[6],paraListData[7],paraListData[8],paraListData[9],
                       paraListData[10],0,paraListData[11],0,paraListData[12],0,paraListData[13],0,paraListData[14],0,
                       0,paraListData[15]
                       )
            self.dbConnWDBCursor.execute(self.strSQL_ITB, valInsert)
            self.dbConnWDB.commit()
            self.entTextInput[0].set("")
            self.entTextInput[1].set("")
        except Exception as e:
            messagebox.showinfo(self.strWinTitle,'Exception occured in committing the database! {}'.format(e))

    def fn_DataInsertTable(self,paraRecordType):
        lstTextFileImgFolder=[]
        lstTextFileImgFolder.append(self.MCQType) #'1' for Signs MCQs and '2' for Rules MCQs
        lstTextFileImgFolder.append(self.entTextInput[0].get()) #For Signs or Rules MCQs, storing in a list, text filename path
        if lstTextFileImgFolder[1]=="":
            messagebox.showinfo(self.strWinTitle, "Text Filename has not been selected to export data to a table!")
            return
        lstTextFileImgFolder.append(self.entTextInput[1].get()) #For Signs or Rules MCQs, storing in a list, images folder path 
        if lstTextFileImgFolder[2]=="":
            messagebox.showinfo(self.strWinTitle, "Images Folder has not been selected to export data to a table!")
            return
        intOptionsCounter = 0
        strExpLines = "N"
        intImageCounter = 1
        lstMCQRec = []
        if self.dbConnWDB is None or self.dbConnWDBCursor is None:
            if self.fn_DBConWithDB()==-1: #Making connection with the database, do nothing if error occurs
                return
        try:
            self.dbConnWDBCursor.execute("SELECT COUNT(*) FROM " + self.strTbName_MCQ + " WHERE MCQ_RecType = " + str(lstTextFileImgFolder[0]))
            recMaxRecNum = self.dbConnWDBCursor.fetchall()
            for curRecLoop in recMaxRecNum:
                intImageCounter = curRecLoop[0] + 1
            rdMCQFile = open(lstTextFileImgFolder[1], "r")
            try:
                for lineRdFile in rdMCQFile:
                    lineRdFile = str(lineRdFile).strip()
                    if lineRdFile[0:1]=="Q" and lineRdFile[1:4].isdecimal()==True and lineRdFile[4:5]=="." and lineRdFile[5:6]==" " and len(lineRdFile[6:])>0:
                        lstMCQRec.clear()
                        lstMCQRec.append(lstTextFileImgFolder[0])
                        lstMCQRec.append(lineRdFile[6:].strip())
                        intOptionsCounter = 0
                        continue
                    if lineRdFile[0:7]=="Image: " and lineRdFile[7:].replace(".","").strip().isdecimal()==True:
                        blobMCQImage = []
                        for intFileCount in range(1,int(lineRdFile[7:].replace(".","").strip())+1):
                            nQImageFile = open(lstTextFileImgFolder[2] + "/" + str(intImageCounter).zfill(3) + "_" + str(intFileCount)+ ".png", "rb")
                            blobMCQImage.append(nQImageFile.read())
                        nQImageFile.close()
                        if len(blobMCQImage)==0:
                            lstMCQRec.append(None)
                            lstMCQRec.append(None)
                        elif len(blobMCQImage)==1:
                            lstMCQRec.append(blobMCQImage[0])
                            lstMCQRec.append(None)
                        elif len(blobMCQImage)==2:
                            lstMCQRec.append(blobMCQImage[0])
                            lstMCQRec.append(blobMCQImage[1])
                        blobMCQImage.clear()
                        lstMCQRec.append(-1)
                        intImageCounter += 1
                        continue
                    if lineRdFile[0:3]=='A. ' and len(lineRdFile[3:])>0:
                        lstMCQRec.append(lineRdFile[3:])
                        intOptionsCounter += 1
                        continue
                    if lineRdFile[0:3]=='B. ' and len(lineRdFile[3:])>0:
                        lstMCQRec.append(lineRdFile[3:])
                        intOptionsCounter += 1
                        continue
                    if lineRdFile[0:3]=='C. ' and len(lineRdFile[3:])>0:
                        lstMCQRec.append(lineRdFile[3:])
                        intOptionsCounter += 1
                        continue
                    if lineRdFile[0:3]=='D. ' and len(lineRdFile[3:])>0:
                        lstMCQRec.append(lineRdFile[3:])
                        intOptionsCounter += 1
                        continue
                    if lineRdFile[0:3]=='E. ' and len(lineRdFile[3:])>0:
                        lstMCQRec.append(lineRdFile[3:])
                        intOptionsCounter += 1
                        continue
                    if lineRdFile[0:1]=="A" and lineRdFile[1:4].isdecimal()==True and lineRdFile[4:5]=="." and lineRdFile[5:6]==" " and len(lineRdFile[6:])>0:
                        lstMCQRec[4] = intOptionsCounter
                        if intOptionsCounter < 5:
                            lstMCQRec.append(None)
                        if intOptionsCounter < 4:
                            lstMCQRec.append(None)
                        if intOptionsCounter < 3:
                            lstMCQRec.append(None)
                        if lineRdFile[6:].count("A")==1:
                            lstMCQRec.append(1)
                        else:
                            lstMCQRec.append(0)
                        if lineRdFile[6:].count("B")==1:
                            lstMCQRec.append(1)
                        else:
                            lstMCQRec.append(0)
                        if lineRdFile[6:].count("C")==1:
                            lstMCQRec.append(1)
                        else:
                            lstMCQRec.append(0)
                        if lineRdFile[6:].count("D")==1:
                            lstMCQRec.append(1)
                        else:
                            lstMCQRec.append(0)
                        if lineRdFile.count("E")==1:
                            lstMCQRec.append(1)
                        else:
                            lstMCQRec.append(0)
                        continue
                    if lineRdFile[0:12]=="Explanation:":
                        strMCQExpDes=lineRdFile
                        strExpLines = "Y"
                        continue
                    if strExpLines == "Y" and len(lineRdFile)>0:
                        strMCQExpDes = strMCQExpDes + " " +lineRdFile
                        continue
                    if strExpLines == "Y" and lineRdFile is None:
                        lstMCQRec.append(strMCQExpDes)
                        strExpLines = "N"
                        self.fn_DataCommitTable(lstMCQRec)
                        continue
                    if strExpLines == "Y" and len(lineRdFile)==0:
                        lstMCQRec.append(strMCQExpDes)
                        strExpLines = "N"
                        self.fn_DataCommitTable(lstMCQRec)
                        continue
                if strExpLines == "Y" and len(lstMCQRec)>0:
                    lstMCQRec.append(strMCQExpDes)
                    strExpLines = "N"
                    self.fn_DataCommitTable(lstMCQRec)
            except Exception as e:
                messagebox.showinfo(self.strWinTitle,'Exception occured! {}'.format(e))
            #Close the Opened text file
            rdMCQFile.close()
        except Exception as e:
            messagebox.showinfo(self.strWinTitle,'Exception occured! {}'.format(e))
            return
        messagebox.showinfo(self.strWinTitle, "File's records with images have been inserted!")
