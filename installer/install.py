import tkinter
from tkinter import ttk, scrolledtext, messagebox,filedialog
import sv_ttk
import os
import psutil
import urllib
from urllib import request
import git
import zipfile
import sh

class installer():
    def __init__(self): # Construct welcome screen
        self.main = tkinter.Tk(None,None," Botemu installer")
        self.main.geometry("600x400+0+0")
        self.main.resizable(False,False)
        sv_ttk.set_theme("dark")
        self.stepBar = ttk.Progressbar(self.main)
        self.stepBar.pack(side = "top",fill = "x")
        self.stepBar.step(20)
        self.welcomeText = tkinter.Label(self.main,text="Welcome to botemu",font = ('TkDefaultFont',18))
        self.welcomeText.pack(side = "top")
        self.explainerText = tkinter.Label(self.main,text="This will install botemu on your machine. Click next to start.")
        self.explainerText.pack(side = "top")
        self.nextFrame = ttk.Frame(self.main)
        self.nextFrame.pack(side = "bottom",fill = "x")
        self.sep = ttk.Separator(self.main)
        self.sep.pack(side = "bottom",fill ="x")        
        self.nextButton = ttk.Button(self.nextFrame,text = "Next",style = "Accent.TButton",command=lambda s = self:s.next())
        self.nextButton.pack(side = "right")
        self.cancelButton = ttk.Button(self.nextFrame,text = "Cancel",command=quit)
        self.cancelButton.pack(side = "left")
        self.main.mainloop()
    def next(self):
        self.stepBar.step(20)
        self.nextButton.config(command=lambda s = self:s.version())
        self.welcomeText.config(text = "EULA")
        self.explainerText.config(text = "Obviously nobody will read this. This software is licensed under GPLV3")
        self.acceptanceVar = 1
        self.rejectButton = ttk.Radiobutton(self.main,text="Decline",value=0,variable=self.acceptanceVar,command=lambda s= self,t=False:s.updateAcceptance(t))
        self.rejectButton.pack(side ="bottom",expand = 1)
        self.acceptButton = ttk.Radiobutton(self.main,text="Accept",value=1,variable=self.acceptanceVar,command=lambda s= self,t=True:s.updateAcceptance(t))
        self.acceptButton.pack(side ="bottom",expand = 1)
        self.mainText = scrolledtext.ScrolledText(self.main)
        self.mainText.pack(side="top",expand=0)
        with open(os.path.join(os.getcwd(),"LICENSE")) as license:
            l = license.read()  
            self.mainText.insert(tkinter.END,l)
        self.mainText.config(state="disabled")
        self.tldrButton = ttk.Button(self.nextFrame,text = "TLDR",command= lambda s = self:s.tldr())
        self.tldrButton.pack(side = "left")
    def version(self):
        self.stepBar.step(20)
        self.acceptButton.pack_forget()
        self.rejectButton.pack_forget()
        self.mainText.pack_forget()
        self.tldrButton.pack_forget()
        self.nextButton.config(command=lambda s = self:s.install())
        self.welcomeText.config(text = "Choose version")
        self.explainerText.config(text="Choose the specifics of your install")
        self.buildVar = "Normal"
        self.buildVarText = tkinter.Label(self.main,text = "Choose build version")
        self.normalBuild = ttk.Radiobutton(self.main,text="Normal/Stable",value = "Normal",variable=self.buildVar,command=lambda s= self,t="Normal":s.updateBuild(t))
        self.normalBuild.pack(side = "top")
        self.betaBuild = ttk.Radiobutton(self.main,text="Beta",value = "Beta",variable=self.buildVar,command=lambda s= self,t="Beta":s.updateBuild(t))
        self.betaBuild.pack(side = "top")
        self.buildOptionExplainerText = tkinter.Label(self.main,text = "Install options")
        self.buildOptionExplainerText.pack(side="top")
        self.portableInstall = False
        self.portableInstallLoc = tkinter.StringVar(self.main,os.getcwd())
        self.makePortableInstall = ttk.Checkbutton(self.main,text= "Make portable version",variable=self.portableInstall,command=lambda s = self:s.portaBuild())
        self.makePortableInstall.pack(side = "top")
        self.internetEnabled = True
        self.useNet = ttk.Checkbutton(self.main,text= "Download from internet (if available)",variable=self.internetEnabled)
        self.useNet.pack(side = "top")
        self.locExplainerText = tkinter.Label(self.main,text = "Porable install options",state="disabled")
        self.locExplainerText.pack(side="top")
        self.dirFrame = ttk.Frame(self.main)
        self.dirFrame.pack(side = "top")
        self.dirEntry = ttk.Entry(self.dirFrame,textvariable = self.portableInstallLoc,state="disabled")
        self.dirEntry.pack(side="left")
        self.dirButton = ttk.Button(self.dirFrame,text="Browse...",command=lambda s = self:self.chooseDir(s),state="disabled")
        self.dirButton.pack(side="right")
    def install(self):
        self.stepBar.step(20)
        self.acceptButton.pack_forget()
        self.rejectButton.pack_forget()
        self.mainText.pack_forget()
        self.tldrButton.pack_forget()
        print("Getting system specs")
        self.welcomeText.config(text = "Installing")
        self.explainerText.config(text="Please wait while we install the program")
        self.progText = tkinter.Label(self.main)
        self.progText.pack(anchor = "center")
        self.progText.config(text="Checking for internet")
        self.progressBar = ttk.Progressbar(self.main)
        self.progressBar.pack(fill = "x",anchor = "center")
        self.hasInternet = False
        self.main.update()
        try:
            request.urlopen("https://www.google.com")
            self.hasInternet = True
            print("User has internet!")
        except:
            self.hasInternet = False
            print("User does not have internet, install from internal package!")
        self.progressBar.step(5)
        self.main.update()
        if self.hasInternet and self.internetEnabled:
            self.progText.config(text="Downloading the app")
            git.Repo.clone_from("https://github.com/bax2004rj/botemu/",os.path.join(os.getcwd(),"installer","temp"))
            self.main.update()
        else:
            self.progText.config(text="Extracting app")
            zipfile.ZipFile.extractall(os.path.join(os.getcwd(),"botemu.zip"),os.path.join(os.getcwd(),"installer","temp"))
            self.main.update()
        self.progText.config(text="Building app")
        self.progressBar.step(25)
        self.main.update()
        self.downloadLocation = os.path.join(os.getcwd(),"installer","temp")
        self.cancelButton.pack_forget()
    def updateAcceptance(self,status):
        if status == True:
            self.nextButton.config(state="normal")
        if status == False:
            self.nextButton.config(state="disabled")
    
    def tldr(self):
        messagebox.showinfo("GPLV3 TLDR","You are free to:\n - do aynything you would like with this (even modify source code!), but please keep the license as-is\n Notice: THIS SOFTWARE HAS NO WARRANTY")

    def updateBuild(self,status):
        self.buildVar = status
    
    def portaBuild(self):
        print(self.portableInstall)
        if self.portableInstall:
            self.dirEntry.config(state = "normal")
            self.dirButton.config(state = "normal")
            self.locExplainerText.config(state = "normal")
        else:
            self.dirEntry.config(state = "disabled")
            self.dirButton.config(state = "disabled")
            self.locExplainerText.config(state = "disabled")

    def chooseDir(self,event = None):
        self.portableInstallLoc.set(filedialog.askdirectory(title="Choose install directory"))

if __name__ == "__main__":
    main = installer()
