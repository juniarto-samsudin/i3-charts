from flask import Blueprint, jsonify
from restdatagenerator.util import generate_temperature,generate_date, response
import simplejson as json

restdatageneratorApp = Blueprint('restdatageneratorApplication', __name__)

@restdatageneratorApp.route("/")
def default():
    #mydata = '{machineName: fanuc,datetime: [2020-07-01 14:14:05, 2020-07-02 00:00:00, 2020-07-03 00:00:00, 2020-07-04 00:00:00],parameters: {temperature: [32, 33, 40, 70]}}'
    myData = {}
    parameters = {}
    temperatureList = generate_temperature()
    datelist = generate_date()
    parameters['temperature'] = temperatureList
    myData['parameters'] = parameters
    myData['datetime'] = datelist
    myData['machineName'] = "fanuc"
    #return jsonify(myData)
    #return json.dumps(myData)
    return response(myData)