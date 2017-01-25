#Handle all UI for the software.

import traceback

from tkinter import *
import tkinter.filedialog as filedialog

import fileop, distance, google, visuals, settings, data_cleaning

def getAddress(data, unit=False):
    ##Feed in a dict of data and return the address.
    if unit and len(str(data["SIT UNIT NUMBER"])) > 0:
        unit = " #"+str(data["SIT UNIT NUMBER"])
    else:
        unit = ""
    house = str(data["SIT HOUSE NUMBER"])+" "+data["SITUS STREET NAME"]+" "+data["SITUS MODE"]+unit
    city = data["SITUS CITY"]+" "+data["SIT STATE"]+" "+str(data["SITUS ZIP CODE"])
    return house+" "+city

class Window():
    #A window to display the application.
    def __init__(self):
        self.root = Tk()
        self.setConfigVars()
        
        #Create and configure the menu.
        self.menubar = Menu(self.root)
        #Create the file menu.
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.loadFile)
        self.filemenu.add_command(label="Save", command=self.saveCurrentInfo)
        self.filemenu.add_command(label="Settings", command = self.settings)
        self.menubar.add_cascade(label = "File", menu = self.filemenu)
        #Create the data menu.
        self.datamenu = Menu(self.menubar, tearoff=0)
        self.datamenu.add_command(label = "Clean Data", command=self.cleanData)
        self.menubar.add_cascade(label = "Data", menu = self.datamenu)

        self.root.config(menu=self.menubar)
        self.root.geometry("600x400")
        #Create and pack the frames.
        self.mainFrame = Frame(self.root, height=480)
        self.mainFrame.pack(fill=BOTH)
        self.leftFrame = Frame(self.mainFrame, width=450, height=480)
        self.leftFrame.pack(side = LEFT, fill=BOTH, expand=1)
        self.rightFrame = Frame(self.mainFrame, width=150, height=480)
        self.rightFrame.pack(side = RIGHT)
        self.bottomFrame = Frame(self.root, height=20, relief = SUNKEN)
        self.bottomFrame.pack(fill=X)

        #Bottom frame:

        #Create the status label.
        self.status = StringVar()
        self.status.set("Ready.")
        self.statusLabel = Label(self.bottomFrame, textvariable = self.status)
        self.statusLabel.pack()

        #Left Frame:

        #Create the "search within" checkbox.
        self.searchWithinVar = IntVar()
        self.searchWithinVar.set(1)
        self.searchWithin = Checkbutton(self.leftFrame, text="Search within radius",
                                        variable = self.searchWithinVar, command=self.searchWithinUpdated)
        self.searchWithin.pack()
        #Create the listbox.
        self.addressList = Listbox(self.leftFrame, height=20)
        self.addressList.pack(fill=BOTH, expand=1)
        #Create the search box.
        self.addressSearchBox = Entry(self.leftFrame)
        self.addressSearchBtn = Button(self.leftFrame, text = "Filter", command = self.searchForAddress)
        self.addressSearchBox.pack(side = LEFT,fill=BOTH, expand=1)
        self.addressSearchBtn.pack(side = RIGHT)

        #Right frame:

        #Create the "Plot Data" checkbox.
        self.plotDataVar = IntVar()
        self.plotData = Checkbutton(self.rightFrame, text = "Plot Data", variable = self.plotDataVar)
        self.plotData.pack()
        #Create the "Radius" section.
        self.radiusFrame = Frame(self.rightFrame)
        self.radiusFrame.pack()
        self.radiusLabel = Label(self.radiusFrame, text = "Search Radius")
        self.radiusLabel.pack(side = LEFT)

        #Create the units drop-down.
        self.variable=StringVar(self.radiusFrame)
        self.variable.set("mi")
        self.radiusUnits = OptionMenu(self.radiusFrame, self.variable, "mi", "km")
        self.radiusUnits.pack(side = RIGHT)
        self.radiusEntry = Entry(self.radiusFrame, width=5)
        self.radiusEntry.pack(side=RIGHT)

        #Create the obstructions only checkbox.
        self.obstructionsOnlyVar = IntVar()
        self.obstructionsOnly = Checkbutton(self.rightFrame, text="Obstructions only", variable = self.obstructionsOnlyVar)
        self.obstructionsOnly.pack()

        #Create the offset section.
        self.offsetFrame = Frame(self.rightFrame)
        self.offsetFrame.pack()
        self.offsetLabel = Label(self.offsetFrame, text = "Offset")
        self.offsetLabel.pack(side=LEFT)
        #Create the units drop-down.
        self.offsetVariable = StringVar(self.offsetFrame)
        self.offsetVariable.set("ft")
        self.offsetUnits = OptionMenu(self.offsetFrame, self.offsetVariable, "ft","m")
        self.offsetUnits.pack(side=RIGHT)
        self.offsetEntry = Entry(self.offsetFrame, width=5)
        self.offsetEntry.pack(side=RIGHT)

        #Create the write to file checkbox and button.
        self.writeToFileVar = IntVar()
        self.writeToFile = Checkbutton(self.rightFrame, text = "Write to file", variable = self.writeToFileVar, command=self.writeCB)
        self.writeToFile.pack()
        self.fileChoose = Button(self.rightFrame, text="Choose file...", command = self.chooseFile, state=DISABLED)
        self.fileChoose.pack()
        self.fileOutput = ""
        #Create the run button.
        self.runBtn = Button(self.rightFrame,text="Run", command=self.runProcess)
        self.runBtn.pack(fill=X, expand=1, side = BOTTOM)
        self.root.title("CoreLogic Grand Challenge")

    def loadFile(self):
        filename = filedialog.askopenfilename(initialdir = self.read_folder)
        if filename=="":
            self.statusUpdate("Please input a valid filename.")
            return
        self.statusUpdate("Opening file...")
        try:
            data = fileop.csvToList(filename,self)
            print(len(data))
        except:
            traceback.print_exc()
            self.statusUpdate("There was an issue loading that file.")
            return
        self.dataListToDisplay(data)
        self.statusUpdate("Ready.")

    def setConfigVars(self):
        self.config = settings.readConfig("config.ini")
        self.google_key = self.config["api"]["google"]
        self.read_folder = self.config["folders"]["read"]
        self.save_folder = self.config["folders"]["save"]

    def cleanData(self):
        data = [i for i in self.addressDict.values()]
        print(len(data))
        self.statusUpdate("Cleaning data...")
        data = data_cleaning.cleanData(data, self)
        self.dataListToDisplay(data)
        self.statusUpdate("Ready.")

    def settings(self):
        win = settings.Settings(self.root)
        self.root.wait_window(win.root)
        self.setConfigVars()

        
    def dataListToDisplay(self, data):
        self.addressDict = {}
        self.addressList.delete(0,END)
        self.statusUpdate("Adding to listbox...")
        for i in data:
            count = 0 #In case the address is already there.
            address = getAddress(i,unit=True)
            a = address
            while a in self.addressDict:
                count += 1
                a = address + " #" + str(count)
            address = a
            self.addressDict[address] = i
            self.addressList.insert(END, address)

    def searchForAddress(self):
        searchTerm = self.addressSearchBox.get().lower()
        addresses = [i for i in self.addressDict.keys()]
        self.addressList.delete(0,END)
        for i in addresses:
            if searchTerm in i.lower():
                self.addressList.insert(END, i)

    def writeCB(self):
        if self.writeToFileVar.get():
            self.fileChoose.config(state=NORMAL)
            self.chooseFile()
        else:
            self.fileChoose.config(text="Choose file...", state=DISABLED)

    def chooseFile(self):
        filename = filedialog.asksaveasfilename(initialdir = self.save_folder)
        if filename == "":
            self.status.set("Please input a file location.")
            self.fileChoose.config(text="Choose file...", state=DISABLED)
            self.writeToFileVar.set(0)
            return
        else:
            self.fileOutput = filename
            niceFilename = filename[filename.rfind("/")+1:]
            self.fileChoose.config(text=niceFilename, state=NORMAL)


    def searchWithinUpdated(self):
        if self.searchWithinVar.get():
            self.updateMainUI(NORMAL)
        else:
            self.updateMainUI(DISABLED)

    def updateMainUI(self, mode):
        #For the searchwithin checkbox.
        self.addressList.config(state=mode)
        self.addressSearchBox.config(state=mode)
        self.addressSearchBtn.config(state=mode)
        self.radiusUnits.config(state=mode)
        self.radiusEntry.config(state=mode)
        self.obstructionsOnly.config(state=mode)
        self.offsetUnits.config(state=mode)
        self.offsetEntry.config(state=mode)
        self.radiusLabel.config(state=mode)
        self.offsetLabel.config(state=mode)


    def statusUpdate(self, message="Ready."):
        #Set the status message at the bottom of the screen.
        self.status.set(message)
        #The screen doesn't update during functions, so force it to update.
        self.statusLabel.update_idletasks()

    def runProcess(self):
        self.statusUpdate("Running...")
        sel = self.addressList.curselection()
        #If the user hasn't selected a property and needs to, alert them.
        if len(sel) == 0 and self.searchWithinVar.get():
            self.status.set("You need to select a property.")
            return
        #If the user is searching within a radius, find every property within that radius.
        if self.searchWithinVar.get():
            #Get the data for the selected property.
            address = self.addressList.get(sel[0])
            data = self.addressDict[address]
            #Pull the lat/long for that property.
            latlong = (data["PARCEL LEVEL LATITUDE"], data["PARCEL LEVEL LONGITUDE"])
            #Try to parse the search radius into a float. If something goes wrong, alert the user.
            if len(self.radiusEntry.get()) == 0:
                self.status.set("You need to input a search radius.")
                return
            try:
                radius = float(self.radiusEntry.get())
                if self.variable.get() == "km":
                    radius = radius/1.60934
            except:
                self.status.set("I cannot understand that search radius.")
                return
            #Once the radius is set, find all houses within the radius of the selected property.
            self.statusUpdate("Finding properties...")
            newData = distance.within([i for i in self.addressDict.values()], latlong, radius)
        #If the user isn't searching within a radius, get all properties.
        else:
            newData = [i for i in self.addressDict.values()]
        #If the user only wants to see properties blocking the view, parse the offset.
        if self.obstructionsOnlyVar.get() and self.searchWithinVar.get():
            #If we're searching for a certain house and want to see only obstructions,
            #Get the offset value and note for later on.
            obstructions = True
            if len(self.offsetEntry.get()) == 0:
                #If they don't specify an offset, assume it's 0.
                offset = 0
            else:
                try:
                    offset = float(self.offsetEntry.get())
                    if self.offsetVariable.get()=="ft":
                        offset = offset*.3048
                except:
                    self.status.set("I cannot understand that offset.")
                    return
        else:
            obstructions = False
        #At this point, newData contains all the properties we are interested in looking at.
        #If elevation is not in the data, use Google to get it.
        #If elevation is in the data, use the existing elevation data.
        if "ELEVATION" not in newData[0].keys():
            dataWithEle = google.getElevations(newData, self.google_key, self)
        else:
            dataWithEle = newData
        #If there isn't elevation data available for some reason (or it is a string), filter it out.
        dataWithEle = [d for d in dataWithEle if "ELEVATION" in d]
        dataWithEle = [d for d in dataWithEle if type(d["ELEVATION"]) != str]
        #If the user wants only obstructions, filter out properties that don't
        #obstruct the view.
        if obstructions:
            self.statusUpdate("Getting obstructions.")
            #Get the elevation of the current address.
            ele = [i["ELEVATION"] for i in dataWithEle if i["PARCEL LEVEL LATITUDE"]==latlong[0] and i["PARCEL LEVEL LONGITUDE"] == latlong[1]][0]
            #Adjust for the offset variable.
            ele = ele - offset
            #Filter out all properties that are greater than the ele variable.
            dataWithEle = [i for i in dataWithEle if i["ELEVATION"]>ele]
        #If we're writing out to a file, write.
        if self.writeToFileVar.get():
            self.statusUpdate("Writing to file...")
            outString = fileop.listToCSV(dataWithEle)
            fileHandle = open(self.fileOutput, "w")
            fileHandle.write(outString)
            fileHandle.close()
        #If we're plotting the data, plot it and display it.
        if self.plotDataVar.get():
            self.statusUpdate("Visualizing data...")
            if self.searchWithinVar.get():
                visuals.visualizeRadius(dataWithEle,latlong, self)
            else:
                visuals.visualizeSet(dataWithEle, self)
                address = "Whole dataset"
            visuals.display(address)
        self.statusUpdate("Ready.")
        return


    def saveCurrentInfo(self):
        #Save all current data to a file.
        filename = filedialog.asksaveasfilename(initialdir = self.save_folder)
        if filename == "":
            self.statusUpdate("Please input a valid filename.")
            return
        outString = fileop.listToCSV([i for i in self.addressDict.values()])
        fileHandle = open(filename, "w")
        fileHandle.write(outString)
        fileHandle.close()
        self.statusUpdate("Ready.")




    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    mainWindow = Window()
    mainWindow.run()
