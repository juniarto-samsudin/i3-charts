from flask import Blueprint
from flask import current_app, Response
import requests
import simplejson as json

mouldfloapiApp = Blueprint('mouldfloapiApplication', __name__)

@mouldfloapiApp.route("/mouldflolive")
def mouldflo_live(machineID, manifoldID, channelID, fieldID, duration):
    API_URL = current_app.config('MOULDFLO_API_URL_LIVE')
    print("API_URL: ", API_URL)
    try:
        r = requests.post(API_URL, data={
            'machineID':machineID,
            'manifoldID':manifoldID,
            'channelID':channelID,
            'fieldID':fieldID,
            'duration': duration}, verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        paramList=[]
        timeList=[]
        status_code=999
        return status_code, paramList, timeList
    else:
        if (r.status_code == 200):
            paramList, timeList = processMouldfloData(r.content)
            return r.status_code, paramList, timeList
        else:
            paramList = []
            timeList = []
            return r.status_code, paramList, timeList

@mouldfloapiApp.route("/mouldflolivejson/<machineID>/<manifoldID>/<channelID>/<fieldID>/<duration>")
def mouldflow_live_json(machineID, manifoldID, channelID, fieldID, duration):
    API_URL = current_app.config('MOULDFLO_API_URL_LIVE')
    print("API_URL: ", API_URL)
    try:
        r = requests.post(API_URL, data={
            'machineID': machineID,
            'manifoldID': manifoldID,
            'channelID': channelID,
            'fieldID': fieldID,
            'duration': duration}, verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        paramList = []
        timeList = []
        status_code = 999
        data = paramList, timeList
        return response(data, 504) #Gateway Timeout
        #return status_code, paramList, timeList
    else:
        if (r.status_code == 200):
            #paramList, timeList = processMouldfloData(r.content)
            #return r.status_code, paramList, timeList
            return response(processMouldfloData(r.content), 200)
        else:
            paramList = []
            timeList = []
            data=paramList,timeList
            #return r.status_code, paramList, timeList
            return response(data, 404) #Not Found

@mouldfloapiApp.route("/mouldflohistorical")
def mouldflo_historical(machineID, manifoldID, channelID, fieldID, starttime, endtime):
    API_URL = current_app.config('MOULDFLO_API_URL_HISTORICAL')
    print("API_URL: ", API_URL)
    try:
        r = requests.post(API_URL, data={
            'machineID':machineID,
            'manifoldID':manifoldID,
            'channelID':channelID,
            'fieldID':fieldID,
            'starttime':starttime,
            'endtime':endtime}, verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        paramList=[]
        timeList=[]
        status_code=999
        return status_code, paramList, timeList
    else:
        if (r.status_code == 200):
            paramList, timeList = processMouldfloData(r.content)
            return r.status_code, paramList, timeList
        else:
            paramList=[]
            timeList=[]
            return r.status_code, paramList, timeList

def processMouldfloData(jsonString):
    '''
    [[{"date":"2020-11-23 17:35:47.000000","timezone_type":3,"timezone":"UTC"},"-0.340"],[{"date":"2020-11-23
17:35:47.000000","timezone_type":3,"timezone":"UTC"},"-0.340"],[{"date":"2020-11-23
17:35:57.000000","timezone_type":3,"timezone":"UTC"},"-0.276"],[{"date":"2020-11-23
17:35:57.000000","timezone_type":3,"timezone":"UTC"},"-0.276"],[{"date":"2020-11-23
17:36:07.000000","timezone_type":3,"timezone":"UTC"},"-0.203"],[{"date":"2020-11-23
17:36:07.000000","timezone_type":3,"timezone":"UTC"},"-0.203"],[{"date":"2020-11-23
    '''
    jsonObj = json.loads(jsonString)
    paramList = []
    timeList = []
    for item in jsonObj:
        paramList.append(float(item[1]))
        timeList.append(item[0]['date'])
    return paramList, timeList

# build a Json response
def response( data, status ):
    return Response( response=json.dumps(data),
                               status=status,
                               mimetype='application/json' )

