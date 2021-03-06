from random import seed
from random import randint
import datetime
from flask  import Response
import simplejson as json
import statistics
import math

def generate_temperature():
    tempList = []
    for _ in range(180):
        temp = randint(100,150)
        tempList.append(temp)
    stdDev = math.floor(statistics.pstdev(tempList))
    return tempList,stdDev

def generate_date():
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours=3)

    inc = datetime.timedelta(minutes=1)
    dateList = []
    myTime = now-delta
    for _ in range(180):
        dateList.append(formatTime(myTime))
        myTime = myTime + inc
    return dateList

def formatTime(time):
    stringTime = time.strftime("%Y-%m-%d %H:%M:%S")
    return stringTime

def generate_upperLimit():
    upperLimitList = []
    for _ in range(180):
        upperLimit = 170
        upperLimitList.append(upperLimit)
    return upperLimitList

def generate_lowerLimit():
    lowerLimitList = []
    for _ in range(180):
        lowerLimit = 80
        lowerLimitList.append(lowerLimit)
    return lowerLimitList

# build a Json response
def response( data ):
    return Response( response=json.dumps(data),
                               status=200,
                               mimetype='application/json' )