from flask import Blueprint
from flask import current_app, Response
import requests
import simplejson as json

externalrestapiApp =  Blueprint('externalrestapiApplication', __name__)


@externalrestapiApp.route("/envlive/<duration>")
def env_live(duration):
    print("inside envlive duration: ", duration)
    API_URL = current_app.config['ENVDATA_API_URL_LIVE']
    try:
        r = requests.post(API_URL, data={'duration': duration}, verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        tempList=[]
        humList=[]
        timeList=[]
        status_code=999
        return status_code, tempList,humList,timeList
    else:
        if (r.status_code == 200):
            tempList, humList, timeList = processEnvData(r.content)
            return r.status_code, tempList, humList, timeList
        else:
            tempList=[]
            humList=[]
            timeList=[]
            return r.status_code, tempList, humList, timeList

@externalrestapiApp.route("/envlivejson/<duration>")
def env_live_json(duration):
    print("inside envlive json duration: ", duration)
    API_URL = current_app.config['ENVDATA_API_URL_LIVE']
    r = requests.post(API_URL, data={'duration': duration}, verify=False)
    return response(processEnvData(r.content))

@externalrestapiApp.route("/envhistorical")
def env_historical(starttime,endtime):
    API_URL = current_app.config['ENVDATA_API_URL_HISTORICAL']
    try:
        r = requests.post(API_URL, data={'starttime': starttime,
                                     'endtime': endtime
                                     },verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        tempList=[]
        humList=[]
        timeList=[]
        status_code=999
        return status_code, tempList, humList, timeList
    else:
        if (r.status_code == 200):
            tempList, humList, timeList = processEnvData(r.content)
            return r.status_code, tempList, humList, timeList
        else:
            tempList=[]
            humList=[]
            timeList=[]
            return r.status_code, tempList, humList, timeList

@externalrestapiApp.route("/fanuclive")
def fanuc_live(machineID, paraIndex, duration):
    API_URL = current_app.config['FANUC_API_URL_LIVE']
    print("FANUC LIVE API-URL: ", API_URL)
    print('MachineID: ', machineID)
    print(paraIndex)
    print(duration)
    try:
        r = requests.post(API_URL, data={
            'machineID':machineID,
            'paraIndex':paraIndex,
            'duration': duration
            }, verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        paramList=[]
        timeList=[]
        status_code=999
        return status_code, paramList, timeList
    else:
        if (r.status_code == 200):
            paramList, timeList = processFanucData(r.content)
            return r.status_code, paramList, timeList
        else:
            paramList=[]
            timeList=[]
            return r.status_code, paramList, timeList

@externalrestapiApp.route("/fanuclivejson/<machineID>/<paraIndex>/<duration>")
def fanuc_live_json(machineID, paraIndex, duration):
    API_URL = current_app.config['FANUC_API_URL_LIVE']
    print("API-URL: ", API_URL)
    print(machineID)
    print(paraIndex)
    print(duration)
    r = requests.post(API_URL, data={
        'machineID':machineID,
        'paraIndex':paraIndex,
        'duration': duration
    }, verify=False)
    return response(processFanucData(r.content))

@externalrestapiApp.route("/fanuchistorical")
def fanuc_historical(machineID, paraIndex, starttime, endtime):
    API_URL = current_app.config['FANUC_API_URL_HISTORICAL']
    print("API-URL: ", API_URL)
    print(machineID)
    print(paraIndex)
    print(starttime)
    print(endtime)
    try:
        r = requests.post(API_URL, data={
            'machineID':machineID,
            'paraIndex':paraIndex,
            'starttime':starttime,
            'endtime':endtime
            },verify=False)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as err:
        paramList=[]
        timeList=[]
        status_code=999
        return status_code, paramList, timeList
    else:
        if (r.status_code == 200):
            paramList, timeList = processFanucData(r.content)
            return r.status_code, paramList, timeList
        else:
            paramList = []
            timeList = []
            return r.status_code, paramList, timeList


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

def processFanucData(jsonString):
    '''
    [[219.89999389648438,{"date":"2020-10-20 03:54:42.000000","timezone_type":3,"timezone":"UTC"}],
    [219.89999389648438,{"date":"2020-10-20 03:54:43.000000","timezone_type":3,"timezone":"UTC"}],
    [219.89999389648438,{"date":"2020-10-20 03:54:44.000000","timezone_type":3,"timezone":"UTC"}],
    [219.89999389648438,{"date":"2020-10-20 03:54:46.000000","timezone_type":3,"timezone":"UTC"}],
    [219.89999389648438,{"date":"2020-10-20 03:54:47.000000","timezone_type":3,"timezone":"UTC"}]]
    '''
    #print('processfanucdata: ', jsonString)
    jsonObj = json.loads(jsonString)
    paramList = []
    timeList = []
    for item in jsonObj:
        paramList.append(item[0])
        timeList.append(item[1]['date'])
    return paramList, timeList

# build a Json response
def response( data ):
    return Response( response=json.dumps(data),
                               status=200,
                               mimetype='application/json' )