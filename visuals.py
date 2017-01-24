##Using matplotlib, visualize the data.

import matplotlib.pyplot as plt
import matplotlib.image as mping
import numpy as np

def visualizeRadius(data, location):
    plt.axis('equal')
    elevationSet = [d["ELEVATION"] for d in data]
    ##Get the range of values covered.
    minval = min(elevationSet)
    maxval = max(elevationSet)
    rangeval = maxval-minval

    for d in data:
        y = d["PARCEL LEVEL LATITUDE"]-location[0]
        x = d["PARCEL LEVEL LONGITUDE"]-location[1]
        p = (d["ELEVATION"]-minval)/rangeval #Percent of where it stands in the elevation graph.
        rgb = (p, 0, 1-p)
        plt.plot([x],[y],"o",color=rgb)
    plt.plot(0,0,"o",color="green")

def visualizeSet(data):
    plt.axis('equal')
    elevationSet = [d["ELEVATION"] for d in data]
    ##Get the range of values covered.
    minval = min(elevationSet)
    maxval = max(elevationSet)
    rangeval = maxval-minval

    for d in data:
        y = d["PARCEL LEVEL LATITUDE"]
        x = d["PARCEL LEVEL LONGITUDE"]
        p = (d["ELEVATION"]-minval)/rangeval #Percent of where it stands in the elevation graph.
        rgb = (p, 0, 1-p)
        plt.plot([x],[y],"o",color=rgb)
    plt.plot(0,0,"o",color="green")

def display(name):
    plt.title(name)
    plt.show(block=False)
