import tkinter
from tkinter import ttk
import sv_ttk
import pygame
import pyperclip

def generateCrashMessage(exception):
    global crashHandler
    pygame.quit()
    crashHandler = tkinter.Tk(None,None," Crash detected!")
    sv_ttk.set_theme("dark")
    crashHandler.geometry("600x500+0+0")
    crashExpText = tkinter.Label(crashHandler,text = "We detected a crash. Below is info about the incident.")
    crashExpText.pack(side="top")
    crashData = ttk.Entry(crashHandler)
    crashData.pack(fill = "both")
    crashData.insert(tkinter.END,exception)
    crashData.config(state="disabled")
    optionsFrame = tkinter.Frame(crashHandler,  bd= 1,relief="raised")
    optionsFrame.pack(side = "bottom",fill = "x")
    restartBtn = ttk.Button(optionsFrame,text="Reopen",style="Accent.TButton")
    restartBtn.pack(side="right")
    closeBtn = ttk.Button(optionsFrame,text="Close",command=quit)
    closeBtn.pack(side="right")
    copyBtn = ttk.Button(optionsFrame,text="Copy",command=lambda e = str(exception): pyperclip.copy(e))
    copyBtn.pack(side="left")
    crashExpTextTwo = tkinter.Label(crashHandler,text = "The app has closed and we sure do hope you saved what you were doing.")
    crashExpTextTwo.pack(side="bottom")
    crashHandler.mainloop()

def reopen():
    global crashHandler
    crashHandler.destroy()
    import main