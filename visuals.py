##Using matplotlib, visualize the data.

import matplotlib.pyplot as plt
import matplotlib.image as mping
import numpy as np

def visualizeRadius(data, location):
    plt.axis('equal')
    elevationSet = [d["ELEVATION"] for d in data]
    elevationSet = [y for y in elevationSet if not isinstance(y, str)]
    ##Get the range of values covered.
    minval = min(elevationSet)
    maxval = max(elevationSet)
    rangeval = maxval-minval

    for d in data:
        rgb = (0,0,0)
        y = d["PARCEL LEVEL LATITUDE"]-location[0]
        x = d["PARCEL LEVEL LONGITUDE"]-location[1]
        try:
            p = (d["ELEVATION"]-minval)/rangeval #Percent of where it stands in the elevation graph.
            if (d.get("isGeo", 0)): #if the data point isn't a house, assign it to a different color scheme
                rgb = (p, 1-p, 0)
            else:
                rgb = (p, 0, 1-p)
            plt.plot([x],[y],"o",color=rgb)
        except:
            continue
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

def display(name, stats):
    plt.title(name)
    plt.show(block=False)
