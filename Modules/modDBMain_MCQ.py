##    This is the main file to run by the user to run the entire program.

import tkinter as tk
from tkinter import messagebox
import os
import modDBOptions_MCQ

if __name__ == "__main__":
    root = tk.Tk() #Setting up the tkinter window
    myDBOpWin = modDBOptions_MCQ.ClassDBOptions(root) #Setting up the DB Options window    
    root.mainloop()
