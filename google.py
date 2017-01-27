#Using Google Maps' API, take a lat/long and return a elevation.

import math
import requests
import json
import userinterface
from geopy.geocoders import GoogleV3

import math

def cleanData(data, window):
    geolocator = GoogleV3(api_key="AIzaSyBdtuUu0mfgQCMDQ8awuW1yEn9b8iGtWmE")
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
	
def elevationPath(api_key, path="36.578581,-118.291994|36.23998,-116.83171",samples="16"):
    url  ="https://maps.googleapis.com/maps/api/elevation/json?path=" + path + "&samples=" + str(int(samples)) + "&key=" + api_key
    r = requests.get(url)
    raw = r.text
    try:
        json_file = json.loads(raw)
    except:
        print(raw)
    elevationList = []
    for resultset in json_file['results']:
        try:
            elevationList.append({"ELEVATION":resultset['elevation'], "PARCEL LEVEL LATITUDE":resultset['location']['lat'], "PARCEL LEVEL LONGITUDE":resultset['location']['lng'], "isGeo":1})
        except:
            print(raw)
            print(url)
    return elevationList

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
	
def getGeoElevations(latlong, api_key, window, radius = 1):
    numSamples = radius*16 #sample every ~100 meters
    radiusEarth = 6378137.0
    geoElevations = []
    strLatLong = str(latlong[0]) + "," + str(latlong[1])
	#fancy alg to find 36 lat/long coords in a 360 degree circle for pathing
    for bearing in range(0, 361, 10):
        dx = radius * math.cos((bearing * math.pi)/180) * 1609
        dy = radius * math.sin((bearing * math.pi)/180) * 1609
		
        dlat = dy/radiusEarth
        dlon = dx/(radiusEarth * math.cos(math.pi * (latlong[0])))
		
        latNew = latlong[0] + ((dlat * 180) / math.pi)
        lonNew = latlong[1] + ((dlon * 180) / math.pi)
		
        path = strLatLong + "|" + str(latNew) + "," + str(lonNew)
		
        geoElevations.extend(elevationPath(api_key, path, numSamples))
    return geoElevations


if __name__=="__main__":
    lat = [(32.872112,-117.249232),(32.872284,-117.244744)]
    api_key = "AIzaSyCYm_XeWvY6xyL_S8qWVF9jNwpYDEjcd1M"
    print(elevation(lat,api_key))
