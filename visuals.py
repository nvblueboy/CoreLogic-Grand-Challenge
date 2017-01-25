##Using matplotlib, visualize the data.

import matplotlib.pyplot as plt
import matplotlib.image as mping
import numpy as np

def visualizeRadius(data, location, window):
    plt.axis('equal')
    plt.clf()
    window.statusUpdate("Getting all elevations...")
    elevationSet = [d["ELEVATION"] for d in data if "ELEVATION" in d]
    elevationSet = [d for d in elevationSet if type(d) != str]
    ##Get the range of values covered.
    minval = min(elevationSet)
    maxval = max(elevationSet)
    rangeval = maxval-minval
    count = 0
    total = len(data)
    oldPercent = 0
    for d in data:
        if "ELEVATION" in d:
            if type(d["ELEVATION"]) != str:
                y = d["PARCEL LEVEL LATITUDE"]-location[0]
                x = d["PARCEL LEVEL LONGITUDE"]-location[1]
                p = (d["ELEVATION"]-minval)/rangeval #Percent of where it stands in the elevation graph.
                rgb = (p, 0, 1-p)
                if y != 'NULL' and x != 'NULL':
                    plt.plot([x],[y],"o",color=rgb)
        count += 1
        percent = round((count/total)*100, 1)
        if oldPercent != percent:
            oldPercent = percent
            window.statusUpdate("Plotting points: "+str(oldPercent)+"%")
    plt.plot(0,0,"o",color="green")

def visualizeSet(data, window):
    plt.axis('equal')
    plt.clf()
    window.statusUpdate("Getting all elevations...")
    elevationSet = [d["ELEVATION"] for d in data if "ELEVATION" in d]
    elevationSet = [d for d in elevationSet if type(d) != str]
    ##Get the range of values covered.
    minval = min(elevationSet)
    maxval = max(elevationSet)
    rangeval = maxval-minval
    count = 0
    total = len(data)
    oldPercent = 0
    for d in data:
        if "ELEVATION" in d:
            if type(d["ELEVATION"]) != str:
                y = d["PARCEL LEVEL LATITUDE"]
                x = d["PARCEL LEVEL LONGITUDE"]
                p = (d["ELEVATION"]-minval)/rangeval #Percent of where it stands in the elevation graph.
                rgb = (p, 0, 1-p)
                if y!='NULL' and x != 'NULL':
                    plt.plot([x],[y],d["ELEVATION"],marker="o",color=rgb)

        count += 1
        percent = round((count/total)*100, 1)
        if oldPercent != percent:
            oldPercent = percent
            window.statusUpdate("Plotting points: "+str(oldPercent)+"%")

def display(name):
    plt.title(name)
    plt.show(block=False)
