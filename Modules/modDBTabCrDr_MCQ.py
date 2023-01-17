##  This file has a class of creating and dropping of the databases.
##  For the program, all the tables of creating and dropping the tables have been performed using this file.

import tkinter as tk
from tkinter import messagebox
import os
import mysql.connector

class ClassDBTabCrDr:
    strDisplayText = "G1 Test"
    dbConnWODB = None
    dbConnWODBCursor = None
    dbConnWDB = None
    dbConnWDBCursor = None
    dbCnHost = ""
    dbCnUser = ""
    dbCnPassword = ""
    strWinTitle = strDisplayText
    strDbName = "dbMCQTest"
    strTbName_MCQ = "dbMCQTest.tbMCQTest"
    strTbName_MCQOnly = "tbMCQTest"
    strTbName_Images = "dbMCQTest.tbImages"
    strTbName_ImagesOnly = "tbImages"
    strTbName_QuizMaster = "dbMCQTest.tbQuizMaster"
    strTbName_QuizMasterOnly = "tbQuizMaster"
    strTbName_QuizDetails = "dbMCQTest.tbQuizDetails"
    strTbName_QuizDetailsOnly = "tbQuizDetails"
    strStatusDB = "DropDatabase"
    strStatusTB_MCQ = "NotExistTable_MCQ"
    strStatusTB_Images = "NotExistTable_Images"
    #strStatusTB_QuizMaster = "NotExistTable_QuizMaster"
    #strStatusTB_QuizDetails = "NotExistTable_QuizDetails"
    strStatusTB_Quiz = "NotExistTables_Quiz"
    strSQL_FindDB = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA WHERE UPPER(SCHEMA_NAME) = '" + strDbName.upper() + "'"
    strSQL_FindTB_MCQ = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND UPPER(TABLE_SCHEMA) = '" + strDbName.upper() + "' AND UPPER(TABLE_NAME) = '" + strTbName_MCQOnly.upper() + "'"
    strSQL_FindTB_Images = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND UPPER(TABLE_SCHEMA) = '" + strDbName.upper() + "' AND UPPER(TABLE_NAME) = '" + strTbName_ImagesOnly.upper() + "'"
    strSQL_FindTB_Quiz = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND UPPER(TABLE_SCHEMA) = '" + strDbName.upper() + "' AND (UPPER(TABLE_NAME) = '" + strTbName_QuizMasterOnly.upper() + "' OR UPPER(TABLE_NAME) = '" + strTbName_QuizDetailsOnly.upper() + "')"
    strSQL_DDB = "DROP DATABASE IF EXISTS " + strDbName.upper()
    strSQL_CDB = "CREATE DATABASE IF NOT EXISTS " + strDbName.upper()
    strSQL_DTB_MCQ = "DROP TABLE IF EXISTS " + strTbName_MCQ.upper()
    strSQL_DTB_Images = "DROP TABLE IF EXISTS " + strTbName_Images.upper()
    strSQL_DTB_QuizMaster = "DROP TABLE IF EXISTS " + strTbName_QuizMaster.upper()
    strSQL_DTB_QuizDetails = "DROP TABLE IF EXISTS " + strTbName_QuizDetails.upper()
    strSQL_CTB_MCQ = "CREATE TABLE " + strTbName_MCQ + " (MCQ_ID INT AUTO_INCREMENT PRIMARY KEY, MCQ_RecActive TINYINT, MCQ_RecType TINYINT, MCQ_QText VARCHAR(255), MCQ_Image1 BLOB, MCQ_Image2 BLOB, MCQ_TotalOptions TINYINT, MCQ_OptText1 VARCHAR(255), MCQ_OptText2 VARCHAR(255), MCQ_OptText3 VARCHAR(255), MCQ_OptText4 VARCHAR(255), MCQ_OptText5 VARCHAR(255), MCQ_AOpt1 TINYINT, MCQ_UOpt1 TINYINT, MCQ_AOpt2 TINYINT, MCQ_UOpt2 TINYINT, MCQ_AOpt3 TINYINT, MCQ_UOpt3 TINYINT, MCQ_AOpt4 TINYINT, MCQ_UOpt4 TINYINT, MCQ_AOpt5 TINYINT, MCQ_UOpt5 TINYINT, MCQ_AnsNum TINYINT, MCQ_AnsExpDes TEXT)"
    strSQL_CTB_Images = "CREATE TABLE " + strTbName_Images + " (Image_ID INT AUTO_INCREMENT PRIMARY KEY, Image_RecActive TINYINT, Image_FileName VARCHAR(255), Image_Data BLOB)"
    strSQL_CTB_QuizMaster = "CREATE TABLE " + strTbName_QuizMaster + " (QuizMaster_ID INT AUTO_INCREMENT PRIMARY KEY, Quiz_RecActive TINYINT, Quiz_UUID VARCHAR(40), Quiz_FirstName VARCHAR(255), Quiz_LastName VARCHAR(255), Quiz_EmailAddress VARCHAR(50), Quiz_StartDateTime DATETIME, Quiz_SubmitDateTime DATETIME, Quiz_SignsResult TINYINT, Quiz_RulesResult TINYINT, Quiz_Total TINYINT)"
    strSQL_CTB_QuizDetails = "CREATE TABLE " + strTbName_QuizDetails + " (QuizDetails_ID INT AUTO_INCREMENT PRIMARY KEY, Quiz_RecActive TINYINT, Quiz_UUID VARCHAR(40), QuizMaster_ID INT, Quiz_SNo TINYINT, MCQ_ID INT, Quiz_RecType TINYINT, Quiz_QText VARCHAR(255), Quiz_Image1 BLOB, Quiz_Image2 BLOB, Quiz_TotalOptions TINYINT, Quiz_OptText1 VARCHAR(255), Quiz_OptText2 VARCHAR(255), Quiz_OptText3 VARCHAR(255), Quiz_OptText4 VARCHAR(255), Quiz_OptText5 VARCHAR(255), Quiz_AOpt1 TINYINT, Quiz_UOpt1 TINYINT, Quiz_AOpt2 TINYINT, Quiz_UOpt2 TINYINT, Quiz_AOpt3 TINYINT, Quiz_UOpt3 TINYINT, Quiz_AOpt4 TINYINT, Quiz_UOpt4 TINYINT, Quiz_AOpt5 TINYINT, Quiz_UOpt5 TINYINT, Quiz_AnsNum TINYINT, Quiz_AnsExpDes TEXT)"
    
    def __init__(self):
        pass

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

    def fn_DrDB(self):
        try:
            if self.dbConnWODB is None:
                self.fn_DBConWithoutDB()
            if self.dbConnWODB is not None:
                intDBExist = 0
                self.strStatusDB = "NotExistDatabase"
                self.dbConnWODBCursor.execute(self.strSQL_FindDB)
                myResult = self.dbConnWODBCursor.fetchall()
                for forCursorDB in myResult:
                    intDBExist = forCursorDB[0]
                if intDBExist==0:
                    messagebox.showinfo(self.strWinTitle, 'Database "' + self.strDbName + '" has not been created! Nothing to drop!')
                    return
                else:
                    messageBoxYesNo = messagebox.askyesno(self.strWinTitle, 'Are you sure to drop the database "' + self.strDbName +'" ?')
                    if messageBoxYesNo==True:
                        self.dbConnWODBCursor.execute(self.strSQL_DDB)
                        self.strStatusDB = "NotExistDatabase"
                        messagebox.showinfo(self.strWinTitle, 'Database "' + self.strDbName + '" has been dropped!')
        except Exception as e:
            messagebox.showinfo(self.strWinTitle, 'Exception occured in dropping the database! {}'.format(e))

    def fn_CrDB(self):
        try:
            if self.dbConnWODB is None:
                self.fn_DBConWithoutDB()
            if self.dbConnWODB is not None:
                intDBExist = 0
                self.strStatusDB = "NotExistDatabase"
                self.dbConnWODBCursor.execute(self.strSQL_FindDB)
                myResult = self.dbConnWODBCursor.fetchall()
                for forCursorDB in myResult:
                    intDBExist = forCursorDB[0]
                if intDBExist!=0:
                    messagebox.showinfo(self.strWinTitle, 'Database "' + self.strDbName + '" has already been created! Nothing to create!')
                    return
                else:
                    messageBoxYesNo = messagebox.askyesno(self.strWinTitle, 'Are you sure to create the database "' + self.strDbName +'"?')
                    if messageBoxYesNo==True:
                        self.dbConnWODBCursor.execute(self.strSQL_CDB)
                        self.strStatusDB = "ExistDatabase"
                        messagebox.showinfo(self.strWinTitle, 'Database "' + self.strDbName + '" has been created!')
        except Exception as e:
            messagebox.showinfo(self.strWinTitle, 'Exception occured in creating the database! {}'.format(e))
            #os._exit(0)

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

    def fn_DrTB_MCQ(self):
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
                    messagebox.showinfo(self.strWinTitle, 'Database "' + self.strDbName + '" has not been created! Nothing to drop!')
                    return
                else:
                    if self.dbConnWDB is None:
                        self.fn_DBConWithDB()
                    if self.dbConnWDB is not None:
                        self.dbConnWDBCursor.execute(self.strSQL_FindTB_MCQ)
                        myResult = self.dbConnWDBCursor.fetchall()
                        for forCursorTB in myResult:
                            intTBExist = forCursorTB[0]
                        if intTBExist==0:
                            messagebox.showinfo(self.strWinTitle, 'Table "' + self.strTbName_MCQOnly + '" has not been created! Nothing to drop!')
                            return
                        else:
                            messageBoxYesNo = messagebox.askyesno(self.strWinTitle, 'Are you sure to drop the table "' + self.strTbName_MCQ +'"?')
                            if messageBoxYesNo==True:
                                self.dbConnWDBCursor.execute(self.strSQL_DTB_MCQ)
                                self.strStatusTB_MCQ = "NotExistTable_MCQ"
                                messagebox.showinfo(self.strWinTitle, 'Table "' + self.strTbName_MCQ + '" has been dropped!')
        except Exception as e:
            messagebox.showinfo(self.strWinTitle, 'Exception occured in dropping the table! {}'.format(e))

    def fn_CrTB_MCQ(self):
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
                    messagebox.showinfo(self.strWinTitle, 'Database "' + self.strDbName + '" has not been created! Nothing to drop!')
                    return
                else:
                    if self.dbConnWDB is None:
                        self.fn_DBConWithDB()
                    if self.dbConnWDB is not None:
                        self.dbConnWDBCursor.execute(self.strSQL_FindTB_MCQ)
                        myResult = self.dbConnWDBCursor.fetchall()
                        for forCursorTB in myResult:
                            intTBExist = forCursorTB[0]
                        if intTBExist!=0:
                            messagebox.showinfo(self.strWinTitle, 'Table "' + self.strTbName_MCQ + '" has already been created! Nothing to create!')
                            return
                        else:
                            messageBoxYesNo = messagebox.askyesno(self.strWinTitle, 'Are you sure to create the table "' + self.strTbName_MCQ +'"?')
                            if messageBoxYesNo==True:
                                self.dbConnWDBCursor.execute(self.strSQL_CTB_MCQ)
                                self.strStatusTB_MCQ = "ExistTable_MCQ"
                                messagebox.showinfo(self.strWinTitle, 'Table "' + self.strTbName_MCQ + '" has been created!')
        except Exception as e:
            messagebox.showinfo(self.strWinTitle, 'Exception occured in creating the table! {}'.format(e))

    def fn_DrTB_Images(self):
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
                    messagebox.showinfo(self.strWinTitle, 'Database "' + self.strDbName + '" has not been created! Nothing to drop!')
                    return
                else:
                    if self.dbConnWDB is None:
                        self.fn_DBConWithDB()
                    if self.dbConnWDB is not None:
                        self.dbConnWDBCursor.execute(self.strSQL_FindTB_Images)
                        myResult = self.dbConnWDBCursor.fetchall()
                        for forCursorTB in myResult:
                            intTBExist = forCursorTB[0]
                        if intTBExist==0:
                            messagebox.showinfo(self.strWinTitle, 'Table "' + self.strTbName_ImagesOnly + '" has not been created! Nothing to drop!')
                            return
                        else:
                            messageBoxYesNo = messagebox.askyesno(self.strWinTitle, 'Are you sure to drop the table "' + self.strTbName_Images +'"?')
                            if messageBoxYesNo==True:
                                self.dbConnWDBCursor.execute(self.strSQL_DTB_Images)
                                self.strStatusTB_Images = "NotExistTable_Images"
                                messagebox.showinfo(self.strWinTitle, 'Table "' + self.strTbName_Images + '" has been dropped!')
        except Exception as e:
            messagebox.showinfo(self.strWinTitle, 'Exception occured in dropping the table! {}'.format(e))

    def fn_CrTB_Images(self):
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
                    messagebox.showinfo(self.strWinTitle, 'Database "' + self.strDbName + '" has not been created! Nothing to drop!')
                    return
                else:
                    if self.dbConnWDB is None:
                        self.fn_DBConWithDB()
                    if self.dbConnWDB is not None:
                        self.dbConnWDBCursor.execute(self.strSQL_FindTB_Images)
                        myResult = self.dbConnWDBCursor.fetchall()
                        for forCursorTB in myResult:
                            intTBExist = forCursorTB[0]
                        if intTBExist!=0:
                            messagebox.showinfo(self.strWinTitle, 'Table "' + self.strTbName_Images + '" has already been created! Nothing to create!')
                            return
                        else:
                            messageBoxYesNo = messagebox.askyesno(self.strWinTitle, 'Are you sure to create the table "' + self.strTbName_Images +'"?')
                            if messageBoxYesNo==True:
                                self.dbConnWDBCursor.execute(self.strSQL_CTB_Images)
                                self.strStatusTB_Images = "ExistTable_Images"
                                messagebox.showinfo(self.strWinTitle, 'Table "' + self.strTbName_Images + '" has been created!')
        except Exception as e:
            messagebox.showinfo(self.strWinTitle, 'Exception occured in creating the table! {}'.format(e))

    def fn_DrTB_Quiz(self):
        try:
            if self.dbConnWODB is None:
                self.fn_DBConWithoutDB()
            if self.dbConnWODB is not None:
                intDBExist = 0
                intTBExist = 0
                self.strStatusDB = "NotExistDatabase"
                self.strStatusTB_Quiz = "NotExistTables_Quiz"
                self.dbConnWODBCursor.execute(self.strSQL_FindDB)
                myResult = self.dbConnWODBCursor.fetchall()
                for forCursorDB in myResult:
                    intDBExist = forCursorDB[0]
                if intDBExist==0:
                    messagebox.showinfo(self.strWinTitle, 'Database "' + self.strDbName + '" has not been created! Nothing to drop!')
                    return
                else:
                    if self.dbConnWDB is None:
                        self.fn_DBConWithDB()
                    if self.dbConnWDB is not None:
                        self.dbConnWDBCursor.execute(self.strSQL_FindTB_Quiz)
                        myResult = self.dbConnWDBCursor.fetchall()
                        for forCursorTB in myResult:
                            intTBExist = forCursorTB[0]
                        if intTBExist==0:
                            messagebox.showinfo(self.strWinTitle, 'Tables "' + self.strTbName_QuizMaster + '" and "' + self.strTbName_QuizDetails + '" have not been created! Nothing to drop!')
                            return
                        else:
                            messageBoxYesNo = messagebox.askyesno(self.strWinTitle, 'Are you sure to drop the tables "' + self.strTbName_QuizMaster + '" and "' + self.strTbName_QuizDetails + '"?')
                            if messageBoxYesNo==True:
                                self.dbConnWDBCursor.execute(self.strSQL_DTB_QuizMaster)
                                self.dbConnWDBCursor.execute(self.strSQL_DTB_QuizDetails)
                                self.strStatusTB_Quiz = "NotExistTables_Quiz"
                                messagebox.showinfo(self.strWinTitle, 'Tables "' + self.strTbName_QuizMaster + '" and "' + self.strTbName_QuizDetails + '" have been dropped!')
        except Exception as e:
            messagebox.showinfo(self.strWinTitle, 'Exception occured in dropping the tables! {}'.format(e))

    def fn_CrTB_Quiz(self):
        try:
            if self.dbConnWODB is None:
                self.fn_DBConWithoutDB()
            if self.dbConnWODB is not None:
                intDBExist = 0
                intTBExist = 0
                self.strStatusDB = "NotExistDatabase"
                self.strStatusTB_Quiz = "NotExistTables_Quiz"
                self.dbConnWODBCursor.execute(self.strSQL_FindDB)
                myResult = self.dbConnWODBCursor.fetchall()
                for forCursorDB in myResult:
                    intDBExist = forCursorDB[0]
                if intDBExist==0:
                    messagebox.showinfo(self.strWinTitle, 'Database "' + self.strDbName + '" has not been created! Nothing to drop!')
                    return
                else:
                    if self.dbConnWDB is None:
                        self.fn_DBConWithDB()
                    if self.dbConnWDB is not None:
                        self.dbConnWDBCursor.execute(self.strSQL_FindTB_Quiz)
                        myResult = self.dbConnWDBCursor.fetchall()
                        for forCursorTB in myResult:
                            intTBExist = forCursorTB[0]
                        if intTBExist!=0:
                            messagebox.showinfo(self.strWinTitle, 'Tables "' + self.strTbName_QuizMaster + '" and "' + self.strTbName_QuizDetails + '" have already been created! Nothing to create!')
                            return
                        else:
                            messageBoxYesNo = messagebox.askyesno(self.strWinTitle, 'Are you sure to create the tables "' + self.strTbName_QuizMaster + '" and "' + self.strTbName_QuizDetails + '"?')
                            if messageBoxYesNo==True:
                                self.dbConnWDBCursor.execute(self.strSQL_CTB_QuizMaster)
                                self.dbConnWDBCursor.execute(self.strSQL_CTB_QuizDetails)
                                self.strStatusTB_Quiz = "ExistTables_Quiz"
                                messagebox.showinfo(self.strWinTitle, 'Tables "' + self.strTbName_QuizMaster + '" and "' + self.strTbName_QuizDetails + '" have been created!')
        except Exception as e:
            messagebox.showinfo(self.strWinTitle, 'Exception occured in creating the tables! {}'.format(e))
