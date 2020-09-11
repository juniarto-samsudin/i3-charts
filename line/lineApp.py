from flask import Blueprint, render_template, request, url_for
from line.util import readCsvFile, readTorquePower
import requests
from restdatagenerator import restdatageneratorApp
import simplejson as json

lineApp = Blueprint("lineApplication", __name__, static_folder="static", template_folder="templates")

@lineApp.route("/<machinename>")
def default(machinename):
    print(request.query_string.decode('utf-8'))
    parameters=request.args.getlist("parameters")
    print("PARAMETERS: ", parameters)
    #example: http://127.0.0.1:5000/line/fanuc?title=juniarto&parameters=temperature&parameters=pressure&parameters=torque
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    title = request.args.get('title')
    lasthours = request.args.get('lasthours')
    freq = request.args.get('freq')
    print("STARTIME: ", starttime)
    print("ENDTIME: ", endtime)
    print("TITLE:", title)
    print("FREQ:",freq)
    if (lasthours):
        print("LASTHOURS: ", lasthours)
        resp = restdatageneratorApp.default() #RESPONSE OBJECT
        mystring = resp.response #STRING
        return render_template('lineTorquePowerLastHour.html', response=mystring, title=title, freq=freq)

    if (machinename == 'testcsv'):
        dateTime, readValue, upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')
        print(readValue)
        print("x:", dateTime[0])
        return render_template('linepage.html', dateTime=dateTime, readValue=readValue, upperLimit=upperLimit,
                           lowerLimit=lowerLimit, setPoint=setPoint)
    elif (machinename == 'fanuc'):
        dateTime, readTorque, readPower = readTorquePower('fanuc-torque-power.csv')
        return render_template('lineTorquePower.html', dateTime=dateTime, readTorque=readTorque, readPower=readPower, title=title, starttime=starttime, endtime=endtime)
    else:
        return render_template('tableNotFound.html')

