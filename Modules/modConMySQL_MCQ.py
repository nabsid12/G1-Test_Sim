##  This file has a class of making connections with MySQL for not only creating and droppping databases and tables,
##  but also retrieving recodrs from tables, and inserting and updating the records of the tables.
##  There are two types of connections have been provided. One without a database name for creating and dropping the database.
##  The other one with a database name for retrieving recodrs from tables, and inserting, updating and deleting
##  the records of the tables.

import tkinter as tk
from tkinter import messagebox
import os
import mysql.connector

class ClassConnectMySQL:
    def __init__(self, master, slave):
        strDisplayText = "G1 Test - MySQL Connection"
        self.master = master
        self.slave = slave
        self.slave.geometry()
        self.slave.resizable(0,0)
        self.slave.title(strDisplayText) #Show title
        self.strWinTitle = strDisplayText
        conFrame = []
        lblList = []
        #lblListString = ["Host","Port","User","Password","auth_plugin"]
        lblListString = ["Host","User","Password"]
        #entListString = ["Mysql@localhost:3306","root","root"]
        #entListString = ["127.0.0.1", "3306","root","root","mysql_native_password"]
        #entListString = ["localhost","root","root"]
        entListString = ["127.0.0.1","root","root"]
        self.entList = []
        self.entTextInput = []
        btnList = []
        btnListString = ["Exit","Connect"]
        for intFrameCounter in range(4):
            conFrame.append(tk.Frame(slave))
            conFrame[intFrameCounter].grid(row=intFrameCounter,columnspan=2)
            if intFrameCounter<3:
                lblList.append(tk.Label(conFrame[intFrameCounter], text = lblListString[intFrameCounter], font=('arial',16,'bold'),
                                     width=6,padx=8,pady=16,bd=8,fg="blue", bg='powder blue',))
                lblList[intFrameCounter].grid(row=intFrameCounter,column=0)
                self.entTextInput.append(tk.StringVar())
                self.entTextInput[intFrameCounter].set(entListString[intFrameCounter])
                self.entList.append(tk.Entry(conFrame[intFrameCounter], textvariable=self.entTextInput[intFrameCounter], justify='left', font=('arial',16,'bold'),
                                    bd=30, insertwidth=4, bg='white',))
                self.entList[intFrameCounter].grid(row=intFrameCounter,column=1)
            else:
                btnList.append(tk.Button(conFrame[intFrameCounter],text = btnListString[0], font=('arial',16,'bold'),
                                      width=6,padx=4,pady=8,bd=16,fg="blue", bg='powder blue',))
                btnList[0].grid(row=intFrameCounter,column=0)
                lblSpacer = tk.Label(conFrame[intFrameCounter], text = "             ",width=6,padx=8,pady=16,bd=8,bg='powder blue',)
                lblSpacer.grid(row=intFrameCounter,column=1)
                btnList.append(tk.Button(conFrame[intFrameCounter],text = btnListString[1], font=('arial',16,'bold'),
                                      width=6,padx=4,pady=8,bd=16,fg="blue", bg='powder blue',))
                btnList[1].grid(row=intFrameCounter,column=2)
        self.dbHost = self.entList[0].get()
        self.dbUser = self.entList[1].get()
        self.dbPassword = self.entList[2].get()
        self.entList[2].configure(show="*") #Hide password entries
        btnList[0].config(fg="red",bg='gold')
        list(map(lambda intVal: btnList[btnListString.index(intVal)].config(command=lambda:self.btnClicked(intVal)), btnListString))
        self.entList[0].focus()

    def fn_DBConWithoutDB(self):
        try:
            self.dbHost = self.entList[0].get()
            self.dbUser = self.entList[1].get()
            self.dbPassword = self.entList[2].get()
            self.dbConnWODB = mysql.connector.connect(
                host = self.dbHost,
                user = self.dbUser,
                password = self.dbPassword
                )
            self.dbConnCursorWODB = self.dbConnWODB.cursor()
            self.master.conHost = self.dbHost
            self.master.conUser = self.dbUser
            self.master.conPassword = self.dbPassword
            messagebox.showinfo(self.strWinTitle,'MySQL connection has been established successfully!')
            self.slave.destroy()
            self.master.update()
            self.master.deiconify()            
        except Exception as e:
            messagebox.showinfo(self.strWinTitle,'Exception occured! Please check entries of Host, User and Password!')

    def btnClicked(self,paraBtn):
        try:
            if paraBtn=="Connect":
                self.fn_DBConWithoutDB()
            elif paraBtn=="Exit":
                msgBoxQ = messagebox.askquestion(self.strWinTitle + ' - Exit MySQL Connection','Are you sure you want to exit MySQL Connection window?',icon = 'warning') 
                if msgBoxQ == 'yes':
                    self.slave.destroy()
                    self.master.update()
                    self.master.deiconify()
        except:
            messagebox.showinfo(self.strWinTitle,'Exception occured! {}'.format(e))
