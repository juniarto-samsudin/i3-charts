import csv
import statistics
import math
import scipy.stats

def readCsvFile(csvfile):
    readTime=[]
    readDate=[]
    dateTime=[]
    readValue=[]
    upperLimit=[]
    lowerLimit=[]
    setPoint=[]
    with open(csvfile) as csvfile:
        csv_reader = csv.reader(csvfile,delimiter=',')
        line_count=0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            else:
                readTime.append(row[0])
                readDate.append(row[1])
                dateTime.append(convertDateTime(row[0],row[1]))
                #print ("DATETIME:", dateTime)
                readValue.append(row[2])
                upperLimit.append(row[3])
                lowerLimit.append(row[4])
                setPoint.append(row[5])
                line_count += 1
    return dateTime, readValue,upperLimit,lowerLimit,setPoint

def readTorquePower(csvfile):
    readTime=[]
    readDate=[]
    dateTime=[]
    readTorque=[]
    readPower=[]
    with open(csvfile) as csvfile:
        csv_reader = csv.reader(csvfile,delimiter=',')
        line_count=0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            else:
                readTime.append(row[0])
                readDate.append(row[1])
                dateTime.append(convertDateTime(row[0], row[1]))
                readTorque.append(float(row[2]))
                readPower.append(float(row[3]))
                line_count += 1
        #print("readtorque: ", readTorque)
        #print("readpower: ", readPower)
        #print("readpowersort: ", sorted(readPower))
        torqueStdDev = math.floor(calcStdDev(readTorque))
        powerStdDev = math.floor(calcStdDev(readPower))
        torqueMean = calcMean(readTorque)
        powerMean = calcMean(readPower)
        xList, yList = genNormalCurve(readPower)
        #print("xList.length = ", len(xList))
        #print("yList.length = ", len(yList))
        #print("xList : ", xList)
        #print("yList : ", yList)
    return dateTime,readTorque,readPower,torqueStdDev,powerStdDev, torqueMean, powerMean, xList, yList

def getStatisticFromList(mylist):
    new_list = []
    #convert damned string to float !FUCK YOUR BACKEND!!!!
    for item in mylist:
        new_list.append(float(item))
    theStdDev = math.floor(calcStdDev(new_list))
    theMean = calcMean(new_list)
    xNormalDistList, yNormalDistList = genNormalCurve(new_list)
    return theStdDev,theMean,xNormalDistList,yNormalDistList

def calcStdDev(data):
    return statistics.stdev(data)

def calcMean(data):
    return statistics.mean(data)

def genNormalCurve(data):
    #X-Axis
    xStart = calcMean(data) - 3*calcStdDev(data)
    xInc = 6*calcStdDev(data)/100 #100 points curve
    xList = []
    xList.append(xStart)
    count  = 0
    while count < 100:
        temp = xList[count] + xInc
        xList.append(temp)
        count = count + 1
    #Y-Axis
    yList = []
    mean = calcMean(data)
    stddev = calcStdDev(data)
    for x in xList:
        #temp = scipy.stats.norm(calcMean(data), calcStdDev(data)).pdf(x)
        temp = scipy.stats.norm(mean,stddev).pdf(x)
        if math.isnan(temp): #artificial data set can result in NAN
            temp=0
        yList.append(temp)
    return xList, yList


def convertDateTime(readTime, readDate):
    myTime = readTime
    myYear = readDate[0:4]
    myMonth = readDate[4:6]
    myDay = readDate[6:8]
    dateResult = myYear+"-"+myMonth+"-"+myDay
    timeDateResult = dateResult + " " + myTime
    return timeDateResult

def addSingleQuote(str):
    mystring = "'" + str + "'"
    return mystring