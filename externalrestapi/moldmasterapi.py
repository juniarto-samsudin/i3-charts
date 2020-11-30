from flask import Blueprint
from flask import current_app, Response
import requests
import simplejson as json

#externalrestapiApp =  Blueprint('externalrestapiApplication', __name__)
moldmasterapiApp = Blueprint('moldmasterapiApplication', __name__)

#@externalrestapiApp.route("/moldmasterlive")
@moldmasterapiApp.route("/moldmasterlive")
def moldmaster_live(machineID, tipID, fieldID, duration):
    API_URL = current_app.config['MOLDMASTER_API_URL_LIVE']
    print("API_URL: ", API_URL)
    print(machineID)
    print(tipID)
    print(fieldID)
    print(duration)
    try:
        r = requests.post(API_URL, data={
            'machineID':machineID,
            'tipID':tipID,
            'fieldID':fieldID,
            'duration': duration}, verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        paramList=[]
        timeList=[]
        status_code=999
        return status_code, paramList, timeList
    else:
        if (r.status_code == 200):
            paramList, timeList = processMoldmasterData(r.content)
            return r.status_code, paramList, timeList
        else:
            paramList = []
            timeList = []
            return r.status_code, paramList, timeList

#@externalrestapiApp.route("/moldmasterlivejson/<machineID>/<tipID>/<fieldID>/<duration>")
@moldmasterapiApp.route("/moldmasterlivejson/<machineID>/<tipID>/<fieldID>/<duration>")
def moldmaster_live_json(machineID, tipID, fieldID, duration):
    API_URL = current_app.config['MOLDMASTER_API_URL_LIVE']
    print("API_URL: ", API_URL)
    try:
        r = requests.post(API_URL, data={
            'machineID':machineID,
            'tipID':tipID,
            'fieldID':fieldID,
            'duration': duration}, verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        print("STATUSCODE999")
        paramList=[]
        timeList=[]
        status_code=999
        return status_code, paramList, timeList
    else:
        if (r.status_code == 200):
            print("STATUSCODE200")
            paramList, timeList = processMoldmasterData(r.content)
            #return r.status_code, paramList, timeList
            return response(processMoldmasterData(r.content), 200)
        else:
            print("STATUSCODEERROR")
            paramList = []
            timeList = []
            return r.status_code, paramList, timeList



#@externalrestapiApp.route("/moldmasterhistorical")
@moldmasterapiApp.route("/moldmasterhistorical")
def moldmaster_historical(machineID, tipID, fieldID, starttime, endtime):
    API_URL = current_app.config['MOLDMASTER_API_URL_HISTORICAL']
    print("API_URL: ", API_URL)
    print(machineID)
    print(tipID)
    print(fieldID)
    print(starttime)
    print(endtime)
    try:
        r = requests.post(API_URL, data={
            'machineID':machineID,
            'tipID':tipID,
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
            paramList, timeList = processMoldmasterData(r.content)
            return r.status_code, paramList, timeList
        else:
            paramList=[]
            timeList=[]
            return r.status_code, paramList, timeList


def processMoldmasterData(jsonString):
    '''
    [{"date":"2020-09-11 11:18:50.000000","timezone_type":3,"timezone":"UTC"},18.399999618530273],[{"date":"2020-09-11
11:19:00.000000","timezone_type":3,"timezone":"UTC"},18.399999618530273],[{"date":"2020-09-11
11:19:10.000000","timezone_type":3,"timezone":"UTC"},18],[{"date":"2020-09-11
11:19:20.000000","timezone_type":3,"timezone":"UTC"},18.799999237060547]
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