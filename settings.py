#Settings modules -- tkinter dialog and config files

import configparser, os
from tkinter import *
import tkinter.filedialog as filedialog

class Settings():
    def __init__(self, parent, filename = "./config.ini"):
        #Create the window and set the basic settings.
        self.root = Toplevel(parent)
        self.root.title("CoreLogic Settings")
        self.filename = filename
        self.parent = parent
        #Check if a file exists, then open it.
        self.configCheck(filename)
        self.config = readConfig(filename)
        #Create and pack the main frame.
        self.mainFrame = Frame(self.root)
        self.mainFrame.pack(fill=BOTH)
        #Create and pack the save and cancel buttons.
        self.buttonFrame = Frame(self.mainFrame, padx=10,pady=10)
        self.buttonFrame.pack(fill=X, side=BOTTOM)
        self.saveButton = Button(self.buttonFrame, text = "OK", command=self.OK)
        self.saveButton.pack(side=LEFT, fill=X, expand=1)
        self.cancelButton = Button(self.buttonFrame, text = "Cancel", command = self.cancel)
        self.cancelButton.pack(side=RIGHT, fill=X, expand=1)
        #Create the Google API frame.
        self.googleFrame = Frame(self.mainFrame, padx = 10, pady=10)
        self.googleFrame.pack(fill=X)
        self.google = StringVar()
        self.google.set(self.config["api"]["google"])
        self.googleLabel = Label(self.googleFrame, text = "Google API Key:")
        self.googleEntry = Entry(self.googleFrame, textvariable=self.google)
        self.googleLabel.pack(side=LEFT)
        self.googleEntry.pack(side=RIGHT, fill=X, expand=1)
        #Create the default folder label.
        self.defaultLabel = Label(self.mainFrame, text = "Default file locations")
        self.defaultLabel.pack()
        #Create the read folder frame.
        self.readFrame = Frame(self.mainFrame, padx=10, pady=5)
        self.readFrame.pack(fill=X)
        self.read = StringVar()
        self.read.set(self.config["folders"]["read"])
        self.readLabel = Label(self.readFrame, text = "Read:")
        self.readEntry = Entry(self.readFrame, textvariable = self.read)
        self.readButton = Button(self.readFrame, text = "...", command=self.readChoose)
        self.readLabel.pack(side=LEFT)
        self.readButton.pack(side=RIGHT)
        self.readEntry.pack(side=RIGHT, fill=X, expand=1)
        #Create the save folder frame.
        self.saveFrame = Frame(self.mainFrame, padx=10, pady=5)
        self.saveFrame.pack(fill=X)
        self.save = StringVar()
        self.save.set(self.config["folders"]["save"])
        self.saveLabel = Label(self.saveFrame, text = "Save:")
        self.saveEntry = Entry(self.saveFrame, textvariable = self.save)
        self.saveButton = Button(self.saveFrame, text="...", command=self.saveChoose)
        self.saveLabel.pack(side=LEFT)
        self.saveButton.pack(side=RIGHT)
        self.saveEntry.pack(side=RIGHT, fill=X, expand=1)
        
    def OK(self):
        #Make sure the specified folders exist.
        read = self.read.get()
        save = self.save.get()
        if not os.path.isdir(read):
            os.makedirs(read)
        if not os.path.isdir(save):
            os.makedirs(save)
        #Write to the ini file.
        self.configSave(self.filename)
        self.root.destroy()

    def cancel(self):
        self.root.destroy()
        
    def readChoose(self):
        file = filedialog.askdirectory()
        self.read.set(file)
        self.root.lift()

    def saveChoose(self):
        file = filedialog.askdirectory()
        self.save.set(file)
        self.root.lift()
        
    def configCheck(self, filename):
        #If the file exists, return. If not, make it.
        if os.path.isfile(filename):
            return
        else:
            currPath = os.path.dirname(os.path.realpath(__file__))
            fileHandle = open(filename, "w")
            string = "[api]\ngoogle=none\n\n[folders]\nread="+currPath+"\\data\nsave="+currPath+"\\data_save"
            fileHandle.write(string)
            fileHandle.close()

    def configSave(self, filename):
        config = configparser.ConfigParser()
        config["api"]={}
        config["folders"] = {}
        config["api"]["google"] = self.google.get()
        config["folders"]["read"] = self.read.get()
        config["folders"]["save"] = self.save.get()
        self.parent.config = config
        with open(filename, "w") as configfile:
            config.write(configfile)
        
    def run(self):
        self.root.mainloop()

def readConfig(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

if __name__ == "__main__":
    s = Settings()
    s.run()
    
