import tkinter
from tkinter import ttk, scrolledtext, messagebox
import sv_ttk
import os
import psutil
import urllib

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
        self.nextFrame = ttk.Frame(self.main,border=1,relief="raised")
        self.nextFrame.pack(side = "bottom",fill = "x")        
        self.nextButton = ttk.Button(self.nextFrame,text = "Next",style = "Accent.TButton",command=lambda s = self:s.next())
        self.nextButton.pack(side = "right")
        self.cancelButton = ttk.Button(self.nextFrame,text = "Cancel",command=quit)
        self.cancelButton.pack(side = "left")  
        self.main.mainloop()
    def next(self):
        self.stepBar.step(20)
        self.nextButton.config(command=lambda s = self:s.specs())
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
    def specs(self):
        self.stepBar.step(20)
        self.acceptButton.pack_forget()
        self.rejectButton.pack_forget()
        self.mainText.pack_forget()
        self.tldrButton.pack_forget()
        print("Getting system specs")
        self.welcomeText.config(text = "System specs")
        self.explainerText.config(text="Please wait while we get system info")
        self.progressBar = ttk.Progressbar(self.main)
        self.progressBar.pack(fill = "x")
        self.hasInternet = False
        self.main.update()
        try:
            urllib.request.urlopen("google.com")
            self.hasInternet = True
            print("User has internet!")
        except:
            self.hasInternet = False
            print("User does not have internet, install from internal package!")
        self.progressBar.step(20)
        self.main.update()
        

    def updateAcceptance(self,status):
        if status == True:
            self.nextButton.config(state="normal")
        if status == False:
            self.nextButton.config(state="disabled")
    
    def tldr(self):
        messagebox.showinfo("GPLV3 TLDR","You are free to:\n - do aynything you would like with this (even modify source code!), but please keep the license as-is\n Notice: THIS SOFTWARE HAS NO WARRANTY")

if __name__ == "__main__":
    main = installer()
