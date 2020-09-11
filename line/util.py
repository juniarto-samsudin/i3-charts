import csv

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
                readTorque.append(row[2])
                readPower.append(row[3])
                line_count += 1
    return dateTime,readTorque,readPower

def convertDateTime(readTime, readDate):
    myTime = readTime
    myYear = readDate[0:4]
    myMonth = readDate[4:6]
    myDay = readDate[6:8]
    dateResult = myYear+"-"+myMonth+"-"+myDay
    timeDateResult = dateResult + " " + myTime
    return timeDateResult