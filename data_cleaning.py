#Data cleaning utilities

import requests
import json
import fileop
import settings

from geopy.geocoders import GoogleV3

def getAddress(data):
    ##Feed in a dict of data and return the address.
    house = str(data["SIT HOUSE NUMBER"])+" "+data["SITUS STREET NAME"]+" "+data["SITUS MODE"]
    city = data["SITUS CITY"]+" "+data["SIT STATE"]+" "+str(data["SITUS ZIP CODE"])
    return house+" "+city

def getGeocodeCensus(address):
    #Use the US Census Bureau's Geocoding Services API to get a coordinate.
    formattedAddress = address.replace(" ","+")
    url = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address="+formattedAddress+"&benchmark=4&format=json"
    r = requests.get(url)
    raw = r.text
    try:
        json_file = json.loads(raw)
        if "exception" in json_file:
            print("yes")
            return tuple()
        if len(json_file["result"]["addressMatches"]) == 0:
            return tuple()
        coords = json_file["result"]["addressMatches"][0]["coordinates"]
        return (coords["y"],coords["x"])
    except:
        print ("Something went wrong. Dumping raw file.")
        print (raw)
        return tuple()

def getGeocodeGoogle(address, key):
    geolocator = GoogleV3(api_key=key)
    try:
        location = geolocator.geocode(address)
        coords = (location.latitude, location.longitude)
    except:
        return tuple()

def cleanData(data, window=None):
    if window != None:
        useWindow = True #If called by user interface, use statusupdate.
    else:
        useWindow = False
    oldPercent = 0
    total = len(data)
    count = 0
    outList = []
    key = settings.readConfig("config.ini")["api"]["google"]
    for d in data:
        if d["PARCEL LEVEL LATITUDE"] == "NULL" or d["PARCEL LEVEL LONGITUDE"] == "NULL":
            ## Try the US Census Bureau. If that doesn't work, try google.
            coords = getGeocodeCensus(getAddress(d))
            success = True
            if len(coords) == 0:
                coords = getGeocodeGoogle(getAddress(d),key)
                if len(coords) == 0:
                    print ("Could not clean data for: "+getAddress(d))
                    success = False
            if success:
                try:
                    d["PARCEL LEVEL LATITUDE"] = coords[0]
                    d["PARCEL LEVEL LONGITUDE"] = coords[1]
                except:
                    print("Something went wrong.")
                    print(coords)
        outList.append(d)
        count += 1
        percent = round((count/total)*100,1)
        if oldPercent != percent:
            oldPercent = percent
            if useWindow:
                window.statusUpdate("Cleaning data: "+str(percent)+"%")
            else:
                print("Cleaning data: "+str(percent)+"%")
    return outList

    
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        filename = input("What file would you like to clean?")
        outFile = input("Where should that file go?")
    elif len(sys.argv) == 3:
        filename = sys.argv[1]
        outFile = sys.argv[2]
    else:
        print ("Usage: "+sys.argv[0]+" [inputfile outputfile]")
        print ("Please specify both files or neither.")
        quit()
    dataInput = fileop.csvToList(filename)
    dataOutput = cleanData(dataInput)
    outStr = fileop.listToCSV(dataOutput)
    fileHandle = open(outFile, "w")
    fileHandle.write(outStr)
    fileHandle.close()
    
    
