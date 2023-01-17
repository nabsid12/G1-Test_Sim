##  This file has a class of exporting image files, icons png, jpeg etc. to a table
##  where it can be used in controls (e.g. buttons and lables) and screens differen from MCQs Quiz.

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
import mysql.connector
#import glob
from pathlib import Path

class ClassExportData_Images:
    def __init__(self, master, slave):
        self.master = master
        self.slave = slave
        self.slave.geometry()
        self.slave.resizable(0,0)
        self.slave.title("G1 Test - Export - Images") #Show title
        self.strWinTitle = "G1 Test - Export - Images"
        self.dbConnWODB = None
        self.dbConnWODBCursor = None
        self.dbConnWDB = None
        self.dbConnWDBCursor = None
        self.dbCnHost = self.master.conHost
        self.dbCnUser = self.master.conUser
        self.dbCnPassword = self.master.conPassword
        self.strDbName = "dbMCQTest"
        self.strTbName_Images = "dbMCQTest.tbImages"
        self.strTbName_ImagesOnly = "tbImages"
        self.strSQL_FindDB = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '" + self.strDbName.upper() + "'"
        self.strSQL_FindTB_Images = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA = '" + self.strDbName.upper() + "' AND TABLE_NAME = '" + self.strTbName_ImagesOnly.upper() + "'"
        self.strSQL_ITB = "INSERT INTO " + self.strTbName_Images + " (Image_RecActive, Image_FileName, Image_Data) VALUES (%s, %s, %s)"
        self.strStatusDB = "NotExistDatabase"
        self.strStatusTB_Images = "NotExistTable_Images"
        dataFrame = []
        self.entTextInput = ""
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
        lblImages = tk.Label(dataFrame[0], text = "Images Folder Path", font=('arial',12,'bold'),
                             width=15,padx=8,pady=16,bd=8,fg="blue", bg='powder blue',)
        lblImages.grid(row=1,column=0)
        btnIF = tk.Button(dataFrame[0],text = "...", font=('arial',10,'bold'),
                              width=3,padx=4,pady=8,bd=16,fg="blue", bg='powder blue',
                              command=lambda:self.fn_ImagesFolderLocation())
        btnIF.grid(row=1,column=1)
        self.entTextInput = tk.StringVar()
        self.entTextInput.set("")
        self.entInput = tk.Entry(dataFrame[0], textvariable=self.entTextInput, justify='left', font=('arial',12,'bold'),
                            width=60, bd=20, insertwidth=8, bg='white', state='disabled',)
        self.entInput.grid(row=1,column=2)
#Ending***********************************************#
#Starting*********************************************#
        dataFrame.append(tk.Frame(slave))
        dataFrame[1].grid(row=2,columnspan=3)
        btnList.append(tk.Button(dataFrame[1],text = btnListString[0], font=('arial',16,'bold'),
                              width=6,padx=4,pady=8,bd=16,fg="blue", bg='powder blue',))
        btnList[0].grid(row=2,column=0)
        lblSpacer = tk.Label(dataFrame[1], text = "             ",width=6,padx=8,pady=16,bd=8,bg='powder blue',)
        lblSpacer.grid(row=2,column=1)
        btnList.append(tk.Button(dataFrame[1],text = btnListString[1], font=('arial',16,'bold'),
                              width=6,padx=4,pady=8,bd=16,fg="blue", bg='powder blue',))
        btnList[1].grid(row=2,column=2)
#Ending***********************************************#
        btnList[0].config(fg="red",bg='gold')
        list(map(lambda intVal: btnList[btnListString.index(intVal)].config(command=lambda:self.btnClicked(intVal)), btnListString))
        #btnList[0].focus()
        self.fn_CheckTB_Images()

    def fn_ImagesFolderLocation(self):
        if self.fn_CheckTB_Images()==False:
            return
        folderImagesPath = filedialog.askdirectory(title=self.strWinTitle,initialdir="/")
        if str(folderImagesPath)!="":
            self.entTextInput.set(str(folderImagesPath))
        else:
            self.entTextInput.set("")
    
    def btnClicked(self,paraBtn):
        try:
            if paraBtn=="Export":
                if self.fn_CheckTB_Images()==False:
                    return
                self.fn_DataInsertTable()
            elif paraBtn=="Exit":
                msgBoxQ = messagebox.askquestion(self.strWinTitle + ' - Exit','Are you sure you want to exit Exporting Images in the Folder window?',icon = 'warning')
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
        
    def fn_CheckTB_Images(self):
        try:
            if self.dbConnWODB is None:
                self.fn_DBConWithoutDB()
            if self.dbConnWODB is not None:
                intDBExist = 0
                intTBExist = 0
                self.strStatusDB = "NotExistDatabase"
                self.strStatusTB_Images = "NotExistTable_Images"
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
                        self.dbConnWDBCursor.execute(self.strSQL_FindTB_Images)
                        myResult = self.dbConnWDBCursor.fetchall()
                        for forCursorTB in myResult:
                            intTBExist = forCursorTB[0]
                        if intTBExist==0:
                            messagebox.showinfo(self.strWinTitle, 'Table "' + self.strTbName_ImagesOnly + '" has not been created! Nothing to export!')
                            return False
                        else:
                            return True
        except Exception as e:
            messagebox.showinfo(self.strWinTitle, 'Exception occured in dropping the table! {}'.format(e))

    def fn_DataInsertTable(self):
        lstMCQRec = []
        iFilePath = ""
        imageFileNameWOE = ""
        blobImageData = None
        if self.entTextInput.get()=="":
            messagebox.showinfo(self.strWinTitle, "Images Folder has not been selected to export data to a table!")
            return
        if self.dbConnWDB is None or self.dbConnWDBCursor is None:
            if self.fn_DBConWithDB()==-1: #Making connection with the database, do nothing if error occurs
                return
        try:
            iFilePath = self.entTextInput.get()
            image_FileNames = os.listdir(iFilePath + "/")
            for iFileName in image_FileNames:
                    imageFileNameWOE = iFileName[:-4]
                    nQImageFile = open(iFilePath + "/" + iFileName, "rb")
                    blobImageData = nQImageFile.read()
                    nQImageFile.close()
                    valInsert = (1, imageFileNameWOE, blobImageData)
                    self.dbConnWDBCursor.execute(self.strSQL_ITB, valInsert)
                    self.dbConnWDB.commit()
            self.entTextInput.set("")
        except Exception as e:
            messagebox.showinfo(self.strWinTitle,'Exception occured in inserting the database! {}'.format(e))
            return
        messagebox.showinfo(self.strWinTitle, "Images in the folder have been inserted!")
