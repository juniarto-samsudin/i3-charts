from flask import Blueprint
from flask import current_app, Response
import requests
import simplejson as json

conairapiApp = Blueprint('conairapiApplication', __name__)

@conairapiApp.route("/conairlive")
def conair_live(machineID, fieldID, duration):
    API_URL = current_app.config["CONAIR_API_URL_LIVE"]
    print("API_URL: ", API_URL)
    try:
        r = requests.post(API_URL, data={
            'machineID':machineID,
            'fieldID':fieldID,
            'duration': duration}, verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        paramList=[]
        timeList=[]
        status_code=999
        return status_code, paramList, timeList
    else:
        if (r.status_code == 200):
            paramList, timeList = processConairData(r.content)
            return r.status_code, paramList, timeList
        else:
            paramList = []
            timeList = []
            return r.status_code, paramList, timeList

@conairapiApp.route("/conairlivejson/<machineID>/<fieldID>/<duration>")
def conair_live_json(machineID, fieldID, duration):
    API_URL = current_app.config["CONAIR_API_URL_LIVE"]
    print("API_URL: ", API_URL)
    try:
        r = requests.post(API_URL, data={
            'machineID': machineID,
            'fieldID': fieldID,
            'duration': duration}, verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        paramList = []
        timeList = []
        status_code = 999
        data = paramList, timeList
        return response(data, 504)
    else:
        if (r.status_code == 200):
            return response(processConairData(r.content), 200)
        else:
            paramList = []
            timeList = []
            data=paramList, timeList
            return response(data, 404)

@conairapiApp.route("/conairhistorical")
def conair_historical(machineID, fieldID, starttime, endtime):
    API_URL = current_app.config['CONAIR_API_URL_HISTORICAL']
    print("API_URL: ", API_URL)
    try:
        r = requests.post(API_URL, data={
            'machineID': machineID,
            'fieldID': fieldID,
            'starttime': starttime,
            'endtime': endtime}, verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        paramList = []
        timeList = []
        status_code = 999
        return status_code, paramList, timeList
    else:
        if (r.status_code == 200):
            paramList, timeList = processConairData(r.content)
            return r.status_code, paramList, timeList
        else:
            paramList = []
            timeList = []
            return r.status_code, paramList, timeList

def processConairData(jsonString):
    '''
  [[{"date":"2020-11-19 11:03:40.000000","timezone_type":3,"timezone":"UTC"},"18.250"],[{"date":"2020-11-19
11:03:40.000000","timezone_type":3,"timezone":"UTC"},"18.250"],[{"date":"2020-11-19
11:04:10.000000","timezone_type":3,"timezone":"UTC"},"18.400"],[{"date":"2020-11-19
11:04:10.000000","timezone_type":3,"timezone":"UTC"},"18.400"],[{"date":"2020-11-19
11:04:41.000000","timezone_type":3,"timezone":"UTC"},"18.560"],[{"date":"2020-11-19
11:04:41.000000","timezone_type":3,"timezone":"UTC"},"18.560"],[{"date":"2020-11-19
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