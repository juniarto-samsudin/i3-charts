from flask import Blueprint
from flask import current_app, Response
import requests
import simplejson as json

cdaapiApp = Blueprint('cdaapiApplication', __name__)

@cdaapiApp.route("/cdalive")
def cda_live(cdaID, fieldID, duration):
    API_URL = current_app.config["CDA_API_URL_LIVE"]
    print("API_URL: ", API_URL)
    try:
        r = requests.post(API_URL, data={
            'cdaID':cdaID,
            'fieldID':fieldID,
            'duration': duration}, verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        paramList=[]
        timeList=[]
        status_code=999
        return status_code, paramList, timeList
    else:
        if (r.status_code == 200):
            paramList, timeList = processCdaData(r.content)
            return r.status_code, paramList, timeList
        else:
            paramList = []
            timeList = []
            return r.status_code, paramList, timeList

@cdaapiApp.route("/cdalivejson/<cdaID>/<fieldID>/<duration>")
def cda_live_json(cdaID, fieldID, duration):
    API_URL = current_app.config["CDA_API_URL_LIVE"]
    print("API_URL: ", API_URL)
    try:
        r = requests.post(API_URL, data={
            'cdaID':cdaID,
            'fieldID':fieldID,
            'duration': duration}, verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        paramList=[]
        timeList=[]
        status_code=999
        data = paramList, timeList
        return response(data, 504)
    else:
        if (r.status_code == 200):
            return response(processCdaData(r.content), 200)
        else:
            paramList = []
            timeList = []
            data=paramList, timeList
            return response(data, 404)

@cdaapiApp.route("/cdahistorical")
def cda_historical(cdaID, fieldID, starttime, endtime):
    API_URL = current_app.config["CDA_API_URL_HISTORICAL"]
    print("API_URL: ", API_URL)
    try:
        r = requests.post(API_URL, data={
            'cdaID':cdaID,
            'fieldID':fieldID,
            'starttime':starttime,
            'endtime':endtime }, verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        paramList=[]
        timeList=[]
        status_code=999
        return status_code, paramList, timeList
    else:
        if (r.status_code == 200):
            paramList, timeList = processCdaData(r.content)
            return r.status_code, paramList, timeList
        else:
            paramList = []
            timeList = []
            return r.status_code, paramList, timeList

def processCdaData(jsonString):
    '''
[[{"date":"2020-11-19 10:23:48.000000","timezone_type":3,"timezone":"UTC"},"18.200"],[{"date":"2020-11-19
10:23:48.000000","timezone_type":3,"timezone":"UTC"},"18.200"],[{"date":"2020-11-19
10:23:58.000000","timezone_type":3,"timezone":"UTC"},"18.200"],[{"date":"2020-11-19
10:23:58.000000","timezone_type":3,"timezone":"UTC"},"18.200"],[{"date":"2020-11-19
10:24:08.000000","timezone_type":3,"timezone":"UTC"},"18.300"],[{"date":"2020-11-19
10:24:08.000000","timezone_type":3,"timezone":"UTC"},"18.300"],[{"date":"2020-11-19
10:24:18.000000","timezone_type":3,"timezone":"UTC"},"18.300"],[{"date":"2020-11-19
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