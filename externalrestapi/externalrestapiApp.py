#from flask import Blueprint
from flask import current_app
import requests
import simplejson as json

#externalrestapiApp =  Blueprint('externalrestapiApplication', __name__)


#@externalrestapiApp.route("/live")
def env_live(duration):
    print("duration: ", duration)
    API_URL = current_app.config['ENVDATA_API_URL_LIVE']
    r = requests.post(API_URL, data={'duration': duration}, verify=False)
    return r.content
#@externalrestapiApp.route("/historical")
def env_historical(starttime,endtime):
    print("starttime: ", starttime)
    print("endtime: ", endtime)
    API_URL = current_app.config['ENVDATA_API_URL_HISTORICAL']
    r = requests.post(API_URL, data={'starttime': starttime,
                                     'endtime': endtime
                                     },verify=False)
    #tempList, humList, timeList = processEnvData(r.content)
    return processEnvData(r.content)
def fanuc_live(duration):
    API_URL = current_app.config['FANUC_API_URL_LIVE']
    return API_URL
def fanuc_historical(starttime, endtime):
    API_URL = current_app.config['FANUC_API_URL_HISTORICAL']
    return API_URL


def processEnvData(jsonString):
    '''
    [[33.29999923706055,66.5999984741211,{"date":"2020-08-14 11:12:12.000000","timezone_type":3,"timezone":"UTC"}],
[33.29999923706055,66.5999984741211,{"date":"2020-08-14 15:05:58.000000","timezone_type":3,"timezone":"UTC"}],
[33.29999923706055,66.5999984741211,{"date":"2020-08-14 15:05:58.000000","timezone_type":3,"timezone":"UTC"}],
[88.80000305175781,88.80000305175781,{"date":"2020-08-14 16:58:05.000000","timezone_type":3,"timezone":"UTC"}]]
    '''
    jsonObj = json.loads(jsonString)
    tempList = []
    humList = []
    timeList = []
    for item in jsonObj:
        tempList.append(item[0]) #temperature
        humList.append(item[1])  #humidity
        timeList.append(item[2]['date'])
    return tempList,humList,timeList

