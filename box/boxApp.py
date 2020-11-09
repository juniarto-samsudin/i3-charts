from flask import Blueprint, render_template, request
from box.util import readCsvFile, addSingleQuote
from restdatagenerator import restdatageneratorApp
from externalrestapi import externalrestapiApp

boxApp = Blueprint("boxApplication", __name__, static_folder="static", template_folder="templates")

@boxApp.route("/historical/<machinename>")
def boxHistorical(machinename):
    # parameters
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    xlabel = request.args.get('xlabel')
    ylabel = request.args.get('ylabel')
    title = request.args.get('title')
    lcl = request.args.get('lcl')
    ucl = request.args.get('ucl')
    sp = request.args.get('sp')
    if machinename == "fanuc":
        machineID = request.args.get('machineID')
        paraIndex = request.args.get('paraIndex')
        envparameter = request.args.get('envparameter')
        starttime = addSingleQuote(starttime)
        endtime = addSingleQuote(endtime)
        print("MACHINEID:", machineID)
        print("paraIndex:", paraIndex)
        print("starttime:", starttime)
        print("endtime:", endtime)
        paramList, dateList = externalrestapiApp.fanuc_historical(int(machineID), int(paraIndex), str(starttime),
                                                                  str(endtime))
        return render_template('boxHistorical.html',
                               dateTime=dateList,
                               plotParameter=paramList,
                               lcl=int(lcl),
                               ucl=int(ucl),
                               sp=int(sp),
                               title=title,
                               ylabel=ylabel,
                               envparameter=envparameter
                               )

@boxApp.route("/live/<machinename>")
def boxLive(machinename):
    # parameters
    duration = request.args.get('duration')
    xlabel = request.args.get('xlabel')
    ylabel = request.args.get('ylabel')
    title = request.args.get('title')
    lcl = request.args.get('lcl')
    ucl = request.args.get('ucl')
    sp = request.args.get('sp')
    freq = request.args.get('freq')
    if machinename == "fanuc":
        machineID = request.args.get('machineID')
        paraIndex = request.args.get('paraIndex')
        envparameter = request.args.get('envparameter')
        paramList, dateList = externalrestapiApp.fanuc_live(machineID, paraIndex, int(duration))
        return render_template('boxLive.html',
                               dateTime=dateList,
                               plotParameter=paramList,
                               title=title,
                               ylabel=ylabel,
                               freq=freq,
                               lcl=lcl,
                               ucl=ucl,
                               sp=sp,
                               envparameter=envparameter,
                               machinename=machinename,
                               machineID=machineID,
                               paraIndex=paraIndex,
                               duration=duration
                               )

@boxApp.route("/<machinename>")
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
    print("STARTIME: ", starttime)
    print("ENDTIME: ", endtime)
    print("TITLE:", title)
    print("FREQ:", freq)
    if (lasthours):
        print("LASTHOURS: ", lasthours)
        resp = restdatageneratorApp.default() #RESPONSE OBJECT
        mystring = resp.response #STRING
        return render_template('boxTorquePowerLastHour.html', response=mystring, title=title, freq=freq)
    if (machinename == "testcsv"):
        dateTime, readValue, upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')
        return render_template("boxpage.html", readValue=readValue)
    else:
        return render_template('tableNotFound.html')