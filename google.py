#Using Google Maps' API, take a lat/long and return a elevation.

import requests
import json
import userinterface
from geopy.geocoders import GoogleV3

import math

def cleanData(data, window):
    geolocator = GoogleV3(api_key="AIzaSyBdtuUu0mfgQCMDQ8awuW1yEn9b8iGtWmE ")
    oldPercent = 0
    count = 0
    total = len(data)
    for d in data:
        if d["PARCEL LEVEL LATITUDE"] == "NULL" or d["PARCEL LEVEL LONGITUDE"] == "NULL":
            a = userinterface.getAddress(d)
            try:
                location = geolocator.geocode(a)
            except:
                continue
            try:
                d["PARCEL LEVEL LATITUDE"] = location.latitude
                d["PARCEL LEVEL LONGITUDE"] = location.longitude
            except:
                print("Couldn't get lat/long for: "+a)
        count+=1
        percent = round((count/total)*100, 1)
        if percent != oldPercent:
            oldPercent = percent
            window.statusUpdate("Cleaning data: "+str(percent)+"%")
    return data


def elevation(data,api_key):
    baseurl = "https://maps.googleapis.com/maps/api/elevation/json?locations="
    latLongList = [(i["PARCEL LEVEL LATITUDE"],i["PARCEL LEVEL LONGITUDE"]) for i in data]
    latLongList = [str(a)+","+str(b) for (a,b) in latLongList if a !="NULL" and b != "NULL"]
    latLongs = "|".join(latLongList)
    url = baseurl+latLongs+"&key="+api_key
    r = requests.get(url)
    raw = r.text
    try:
        json_file = json.loads(raw)
    except:
        print(raw)
    for i in range(len(latLongList)):
        try:
            data[i]["ELEVATION"] = json_file["results"][i]["elevation"]
        except:
            print(raw)
            print(url)
            input()
    return {"results":data,"status":r.status_code}

def getElevations(data, api_key, window, toRun = 256):
    amt = len(data)
    runs = math.ceil(amt/toRun)
    num = 0
    runNum = 0
    results = []
    while num+toRun < amt:
        window.statusUpdate("Getting elevations: "+str(round((runNum/runs)*100,2))+"%")
        ele = elevation(data[num:num+toRun],api_key)
        results = results+ele["results"]
        num += toRun
        runNum += 1
    ele = elevation(data[num:],api_key)
    results = results + ele["results"]
    window.statusUpdate("Retrieved elevations.")
    return results


if __name__=="__main__":
    lat = [(32.872112,-117.249232),(32.872284,-117.244744)]
    api_key = "AIzaSyCYm_XeWvY6xyL_S8qWVF9jNwpYDEjcd1M"
    print(elevation(lat,api_key))
