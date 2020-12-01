from flask import Blueprint
from flask import current_app, Response
import requests
import simplejson as json

motanapiApp = Blueprint('motanapiApplication', __name__)

@motanapiApp.route("/motanlive")
def motan_live(machineID, fieldID, duration):
    API_URL = current_app.config["MOTAN_API_URL_LIVE"]
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
            paramList, timeList = processMotanData(r.content)
            return r.status_code, paramList, timeList
        else:
            paramList = []
            timeList = []
            return r.status_code, paramList, timeList

@motanapiApp.route("/motanlivejson/<machineID>/<fieldID>/<duration>")
def motan_live_json(machineID, fieldID, duration):
    API_URL = current_app.config["MOTAN_API_URL_LIVE"]
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
            return response(processMotanData(r.content),200)
        else:
            paramList = []
            timeList = []
            data=paramList, timeList
            return response(data, 404)

@motanapiApp.route("/motanhistorical")
def motan_historical(machineID, fieldID, starttime, endtime):
    API_URL = current_app.config['MOTAN_API_URL_HISTORICAL']
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
            paramList, timeList = processMotanData(r.content)
            return r.status_code, paramList, timeList
        else:
            paramList = []
            timeList = []
            return r.status_code, paramList, timeList



def processMotanData(jsonString):
    '''
    [[{"date":"2020-10-01 09:00:23.000000","timezone_type":3,"timezone":"UTC"},"100.000"],[{"date":"2020-10-01
09:00:53.000000","timezone_type":3,"timezone":"UTC"},"100.000"],[{"date":"2020-10-01
09:01:23.000000","timezone_type":3,"timezone":"UTC"},"100.000"],[{"date":"2020-10-01
09:01:53.000000","timezone_type":3,"timezone":"UTC"},"100.000"],[{"date":"2020-10-01
09:02:23.000000","timezone_type":3,"timezone":"UTC"},"100.000"],[{"date":"2020-10-01
09:02:53.000000","timezone_type":3,"timezone":"UTC"},"100.000"],[{"date":"2020-10-01
09:03:23.000000","timezone_type":3,"timezone":"UTC"},"100.000"],[{"date":"2020-10-01
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