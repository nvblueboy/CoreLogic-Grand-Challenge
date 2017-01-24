##Taking a list of dictionaries, get all houses within a certain distance of a certain lat/long.

import requests

from geopy.distance import vincenty

def within(data, latlong, radius=1):
    outList = []
    for i in data:
        latlong_i = (i["PARCEL LEVEL LATITUDE"],i["PARCEL LEVEL LONGITUDE"])
        if "NULL" in latlong_i:
            ## TODO: Make a google call based on the address.
            continue
        dist = vincenty(latlong, latlong_i).miles
        if dist<=radius:
            outList.append(i)
    return outList


