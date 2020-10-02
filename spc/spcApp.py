from flask import Blueprint, render_template, request
from spc.util import readCsvFile, readTorquePower
from restdatagenerator import restdatageneratorApp

spcApp = Blueprint("spcApplication", __name__, static_folder="static", template_folder="templates")

@spcApp.route("/<machinename>")
def default(machinename):
    print(request.query_string.decode('utf-8'))
    parameters = request.args.getlist("parameters")
    print("PARAMETERS: ", parameters)
    # example: http://127.0.0.1:5000/line/fanuc?title=juniarto&parameters=temperature&parameters=pressure&parameters=torque
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    title = request.args.get('title')
    lasthours = request.args.get('lasthours')
    freq = request.args.get('freq')
    titlex = request.args.get('titlex')
    titley = request.args.get('titley')
    print("STARTIME: ", starttime)
    print("ENDTIME: ", endtime)
    print("TITLE:", title)
    print("FREQ:", freq)
    if (lasthours):
        print("LASTHOURS: ", lasthours)
        resp = restdatageneratorApp.default() #RESPONSE OBJECT
        mystring = resp.response #STRING
        return render_template('spcTorquePowerLastHour.html', response=mystring, title=title, freq=freq)
    if (machinename == "testcsv"):
        dateTime, readValue, upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')
        return render_template('spcpage.html', dateTime=dateTime, readValue=readValue, upperLimit=upperLimit,
                               lowerLimit=lowerLimit, setPoint=setPoint)
    elif (machinename == 'fanuc'):
        dateTime, readTorque, readPower, torqueStdDev, powerStdDev, torqueMean, powerMean,xList, yList = readTorquePower('fanuc-torque-power.csv')
        print("torquestddev: ", torqueStdDev)
        print("powerstddev: ", powerStdDev )
        print("torquemean: ", torqueMean)
        print("powermean: ", powerMean)
        return render_template('spcTorquePower.html', dateTime=dateTime, readTorque=readTorque, readPower=readPower, torqueStdDev=torqueStdDev, powerStdDev=powerStdDev, torqueMean=torqueMean, powerMean=powerMean, title=title, titlex=titlex, titley=titley,xList=xList, yList=yList, starttime=starttime, endtime=endtime)
    else:
        return render_template('tableNotFound.html')