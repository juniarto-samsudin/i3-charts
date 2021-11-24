from flask import Blueprint
from flask import current_app, Response
import requests
import simplejson as json

predapiApp = Blueprint('predapiApplication', __name__)

@predapiApp.route('/predlive')
def pred_live(machineID, duration):
   API_URL = current_app.config["PRED_API_URL_LIVE"]
   print("INSIDE PRED LIVE: ", API_URL)
   try:
        r = requests.post(API_URL, data={
            'machineID':machineID,
            'duration': duration}, verify=False)
   except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        paramList=[]
        timeList=[]
        status_code=999
        return status_code, paramList, timeList
   else:
        if (r.status_code == 200):
            paramList, timeList = processPredData(r.content)
            return r.status_code, paramList, timeList
        else:
            paramList = []
            timeList = []
            return r.status_code, paramList, timeList

@predapiApp.route('/predlivejson/<machineID>/<duration>')
def pred_live_json(machineID, duration):
    API_URL = current_app.config["PRED_API_URL_LIVE"]
    print("INSIDE PRED LIVE JSON: ", API_URL)
    try:
        r = requests.post(API_URL, data={
            'machineID': machineID,
            'duration': duration}, verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        paramList = []
        timeList = []
        status_code = 999
        data = paramList, timeList
        return response(data, 504)
    else:
        if (r.status_code == 200):
            return response(processPredData(r.content), 200)
        else:
            paramList = []
            timeList = []
            data=paramList, timeList
            return response(data, 404)

@predapiApp.route("/predhistorical")
def pred_historical(machineID, starttime, endtime):
    API_URL = current_app.config['PRED_API_URL_HISTORICAL']
    print("INSIDE PRED HISTORICAL: ", API_URL)
    print('MACHINE ID: ', machineID)
    print('STARTTIME: ', starttime)
    print('END TIME: ', endtime)
    try:
        r = requests.post(API_URL, data={
            'machineID': machineID,
            'startdate': starttime,
            'enddate': endtime
        }, verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        paramList=[]
        timeList=[]
        status_code=999
        return status_code, paramList, timeList
    else:
        if (r.status_code == 200):
            paramList, timeList = processPredData(r.content)
            return r.status_code, paramList, timeList
        else:
            paramList = []
            timeList = []
            return r.status_code, paramList, timeList

def processPredData(jsonString):
    '''
    [[{"date":"2021-05-24 15:27:30.000000","timezone_type":3,"timezone":"UTC"},"1"],[{"date":"2021-05-24
15:28:52.000000","timezone_type":3,"timezone":"UTC"},"1"],[{"date":"2021-05-24
15:29:17.000000","timezone_type":3,"timezone":"UTC"},"1"]]
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