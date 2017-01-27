#Output a KML file with the data.

def visualizeEarth(data, filename, window=None):
    if window != None:
        useWindow = True
    else:
        useWindow = False
    elevationSet = [d["ELEVATION"] for d in data if "ELEVATION" in d]
    elevationSet = [d for d in elevationSet if type(d) != str]
    ##Get the range of values covered.
    minval = min(elevationSet)
    maxval = max(elevationSet)
    rangeval = maxval-minval
    step = rangeval / 256
    count = 0
    total = len(data)
    oldPercent = 0
    points = [] #To store the points for output to KML.
    pointList = [minval + (step * i) for i in range(256)]
    for d in data:
        if "ELEVATION" not in d:
            continue
        if type(d["ELEVATION"]) == str:
            continue
        colorVal = 0
        eleVal = d["ELEVATION"]
        for i in range(255):
            if pointList[i+1] > eleVal and pointList[i] < eleVal:
                colorVal = i
                break
            if i == 254:
                point = 255
                break
        points.append((colorVal, d))
        count += 1
        percent = round((count/total)*100, 0)
        if oldPercent != percent:
            oldPercent = percent
            if useWindow:
                window.statusUpdate("Getting elevation values: "+str(oldPercent)+"%")
            else:
                print("Getting elevation values: "+str(oldPercent)+"%")
    diamonds = []
    for point in points:
        if point[1]["PARCEL LEVEL LATITUDE"] == "NULL" or point[1]["PARCEL LEVEL LONGITUDE"] == "NULL":
            continue
        latlong = (point[1]["PARCEL LEVEL LATITUDE"],point[1]["PARCEL LEVEL LONGITUDE"])
        diamonds.append((pointDiamond(latlong),point))
    #Now that all the info is available, format to a string and print.
    colorString = ""
    polyString = ""
    colors = set()
    total = len(diamonds)
    count = 0
    oldPercent = 0
    for diamond in diamonds:
        color = diamond[1][0]
        if color not in colors:
            colorString = colorString + colorToString(pointToHex(color)) + "\n"
            colors.add(color)
        polyString = polyString + diamondToString(diamond[0],pointToHex(color)) + "\n"
        count += 1
        percent = round((count/total)*100, 0)
        if oldPercent != percent:
            oldPercent = percent
            if useWindow:
                window.statusUpdate("Printing to file: "+str(oldPercent)+"%")
            else:
                print("Printing to file: "+str(oldPercent)+"%")
    fileHandle = open(filename,mode="w")
    fileHandle.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>'+colorString+polyString+'</Document></kml>')
    fileHandle.close()
    return "Done."


            
def colorToString(hexcode):
    return '<Style id="'+hexcode+'"><LineStyle><width>1.5</width><color>ff'+hexcode+'</color></LineStyle><PolyStyle><color>7d'+hexcode+'</color></PolyStyle></Style>'

def diamondToString(diamond, hexcode):
    string_p1 = '<Placemark><styleUrl>#'+hexcode+'</styleUrl><Polygon><altitudeMode>relativeToGround</altitudeMode><outerBoundaryIs><LinearRing><coordinates>'
    string_p2 = diamond+'</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>'
    return string_p1+string_p2
                        

def pointDiamond(latlong):
    up = str(latlong[1])+","+str(latlong[0]+.0001)+",5\n"
    down = str(latlong[1])+","+str(latlong[0]-.0001)+",5\n"
    left = str(latlong[1]+.0001)+","+str(latlong[0])+",5\n"
    right = str(latlong[1]-.0001)+","+str(latlong[0])+",5\n"
    return up+left+down+right+up
            
def pointToHex(point):
    first = hex(255-point)[2:]
    if len(first)==1:
        first = "0"+first
    last = hex(point)[2:]
    if len(last)==1:
        last = "0"+last
    return first+"00"+last

if __name__ == "__main__":
    import fileop
    filename = "./data_save/data_clean_save.csv"
    dataList = fileop.csvToList(filename)
    print(visualizeEarth(dataList[:10000], "C:/Users/Dylan/Desktop/test.kml"))
