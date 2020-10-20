from flask import Blueprint, render_template, request
from spc.util import readCsvFile, readTorquePower, getStatisticFromList
from restdatagenerator import restdatageneratorApp
from externalrestapi import externalrestapiApp

spcApp = Blueprint("spcApplication", __name__, static_folder="static", template_folder="templates")

@spcApp.route("/historical/<machinename>")
def spcHistorical(machinename):
    #parameters
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    xlabel = request.args.get('xlabel')
    ylabel = request.args.get('ylabel')
    title = request.args.get('title')
    lcl = request.args.get('lcl')
    ucl = request.args.get('ucl')
    sp = request.args.get('sp')
    #get-data
    if machinename == "envdata":
        envparameter = request.args.get('envparameter') #humidity or temperature
        tempList, humList, dateList = externalrestapiApp.env_historical(starttime, endtime)
        if envparameter == "temperature":
            StdDev, Mean, xNormDistList, yNormDistList = getStatisticFromList(tempList)
            return render_template('spcHistorical.html',
                                    dateTime=dateList,
                                    plotParameter=tempList,
                                    StdDev = StdDev,
                                    lcl = int(lcl),
                                    ucl = int(ucl),
                                    sp = int(sp),
                                    title=title,
                                    ylabel=ylabel,
                                    xNormalDistList=xNormDistList,
                                    yNormalDistList=yNormDistList,
                                    envparameter = envparameter
                                   )
        elif envparameter == "humidity":
            StdDev, Mean, xNormDistList, yNormDistList = getStatisticFromList(humList)
            return render_template('spcHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=humList,
                                   StdDev=StdDev,
                                   lcl=int(lcl),
                                   ucl=int(ucl),
                                   sp=int(sp),
                                   title=title,
                                   ylabel=ylabel,
                                   xNormalDistList=xNormDistList,
                                   yNormalDistList=yNormDistList,
                                   envparameter=envparameter)
            # return render_template('spcHistorical.html', dateTime=dateTime, readTorque=readTorque, readPower=readPower,
            #                        torqueStdDev=torqueStdDev, powerStdDev=powerStdDev, torqueMean=torqueMean,
            #                        powerMean=powerMean, title=title, titlex=titlex, titley=titley, xList=xList,
            #                        yList=yList,
            #                        starttime=starttime, endtime=endtime)
    elif machinename == "fanuc":
        resp = externalrestapiApp.fanuc_historical(starttime, endtime)
        return resp

@spcApp.route("/live/<machinename>")
def spcLive(machinename):
    #parameters
    duration = request.args.get('duration')
    xlabel = request.args.get('xlabel')
    ylabel = request.args.get('ylabel')
    title = request.args.get('title')
    lcl = request.args.get('lcl')
    ucl = request.args.get('ucl')
    sp = request.args.get('sp')
    #get-data
    if machinename == "envdata":
        resp = externalrestapiApp.env_live(int(duration))
        return resp
    elif machinename == "fanuc":

        resp = externalrestapiApp.fanuc_live(int(duration))
        return resp


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
