##Read the CSV file into a list of dictionaries.


def csvToList(filename, window, header=True):
    ## Set header to false if there are no headers.

    ## Read the file into a list of lines.
    fileHandle=open(filename,"r")
    lines = fileHandle.readlines()
    fileHandle.close()
    ## Initialize the output list.
    outputList = []
    ## If there are headers in the file, set the header list to the headers.
    if header:
        headerList = lines[0].split(",")
    ## If there are not headers, just set them to 0, 1, 2, 3, 4...
    else:
        headerList = range(len(lines[0].split(",")))
        ##Also add the first line to the output list.
        outputList.append(createDict(lines[0],headerList))
    oldPercent = 0
    count=0
    total=len(lines)
    for i in lines[1:]:
        ##For each line, add the created dictionary to the list.
        outputList.append(createDict(i,headerList))
        count += 1
        percent = round((count/total)*100,1)
        if percent != oldPercent:
            oldPercent = percent
            window.statusUpdate("Creating dictionaries: "+str(oldPercent)+"%")
    return outputList


def createDict(line, headers):
    #Take a string input and a header list and make a dictionary.
    outputDict = {}
    line = line.split(",")
    for i in range(len(line)):
        ## If you can return a float, return a float.
        ## If converstion to an int isn't lossy, return an int.
        ## Otherwise, return a string.
        data = line[i].replace("\n","") ## Set data and remove line breaks.
        try:
            data = float(data) ## Convert to a float.
            if int(data) == data:
                data = int(data) ## If int(i) == i, i must be an integer.
        except:
            pass
        outputDict[headers[i]] = data
    return outputDict

def listToCSV(data):
    keySet = set()
    #Get a set of all keys.
    for i in data:
        for j in i:
            keySet.add(j)
    keyList=sorted(list(keySet)) #To put in alphabetical order.
    outList = [[i for i in keyList]]
    size = len(keyList)
    for d in data:
        partialList = ["" for i in keyList]
        for i in range(len(keyList)):
            if keyList[i] in d:
                partialList[i] = d[keyList[i]]
        outList.append(partialList)
    outStr = ""
    for line in outList:
        outStr += ",".join([str(i).replace("\n","") for i in line]) + "\n"
    return outStr

if __name__ == "__main__":
    lists = [{"a":1,"b":2, "c":3},{"b":3},{"c":5,"a":2}]
    print(listToCSV(lists))
