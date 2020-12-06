from flask import Blueprint, render_template, request
from histogram.util import readCsvFile, readTorquePower, addSingleQuote
from spc.util import getStatisticFromList
from restdatagenerator import restdatageneratorApp
from externalrestapi import externalrestapiApp, moldmasterapi, mouldfloapi, motanapi, conairapi, cdaapi

histoApp = Blueprint("histoApplication", __name__, static_folder="static", template_folder="templates")

'''
╦ ╦╦╔═╗╔╦╗╔═╗╦═╗╦╔═╗╔═╗╦  
╠═╣║╚═╗ ║ ║ ║╠╦╝║║  ╠═╣║  
╩ ╩╩╚═╝ ╩ ╚═╝╩╚═╩╚═╝╩ ╩╩═╝
'''

@histoApp.route("/historical/<machinename>")
def histoHistorical(machinename):
    # parameters
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    xlabel = request.args.get('xlabel')
    ylabel = request.args.get('ylabel')
    title = request.args.get('title')
    lcl = request.args.get('lcl')
    ucl = request.args.get('ucl')
    sp = request.args.get('sp')
    if machinename == "envdata":
        print("INSIDE ENVDATA HISTOGRAM HISTORICAL")
        envparameter = request.args.get('envparameter')  # humidity or temperature
        statusCode, tempList, humList, dateList = externalrestapiApp.env_historical(starttime, endtime)
        if (statusCode == 200):
            if envparameter == "temperature":
                return render_template('histoHistorical.html',
                                       dateTime=dateList,
                                       plotParameter=tempList,
                                       lcl=int(lcl),
                                       ucl=int(ucl),
                                       sp=int(sp),
                                       title=title,
                                       ylabel=ylabel,
                                       envparameter=envparameter,
                                       )
            elif envparameter == "humidity":
                return render_template('histoHistorical.html',
                                       dateTime=dateList,
                                       plotParameter=humList,
                                       lcl=int(lcl),
                                       ucl=int(ucl),
                                       sp=int(sp),
                                       title=title,
                                       ylabel=ylabel,
                                       envparameter=envparameter,
                                       )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "fanuc":
        machineID = request.args.get('machineID')
        paraIndex = request.args.get('paraIndex')
        envparameter = request.args.get('envparameter')
        starttime = addSingleQuote(starttime)
        endtime = addSingleQuote(endtime)
        print("MACHINEID:", machineID)
        print("paraIndex:", paraIndex)
        print("starttime:", starttime)
        print("endtime:", endtime)
        statusCode,paramList, dateList = externalrestapiApp.fanuc_historical(int(machineID), int(paraIndex), str(starttime),
                                                                  str(endtime))
        if (statusCode == 200):
            StdDev, Mean, xNormDistList, yNormDistList = getStatisticFromList(paramList)
            return render_template('histoHistorical.html',
                               dateTime=dateList,
                               plotParameter=paramList,
                               lcl=int(lcl),
                               ucl=int(ucl),
                               sp=int(sp),
                               title=title,
                               ylabel=ylabel,
                               envparameter=envparameter,
                               StdDev=StdDev,
                               Mean=Mean,
                               xNormalDistList=xNormDistList,
                               yNormalDistList=yNormDistList
                               )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "moldmaster":
        print ("INSIDE HISTO MOLDMASTER HISTORICAL")
        machineID = request.args.get('machineID')
        tipID = request.args.get('tipID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        noCL = request.args.get('noCL')
        starttime = addSingleQuote(starttime)
        endtime = addSingleQuote(endtime)
        print("MACHINEID:", machineID)
        print("starttime:", starttime)
        print("endtime:", endtime)
        statusCode, paramList, dateList = moldmasterapi.moldmaster_historical(machineID, tipID, fieldID, starttime,
                                                                              endtime)
        if (statusCode == 200):
            print('status-code: ', statusCode)
            return render_template('histoHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   title=title,
                                   ylabel=ylabel,
                                   envparameter=envparameter
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "mouldflo":
        print("INSIDE  HISTOGRAM MOULDFLO-HISTORICAL")
        machineID = request.args.get('machineID')
        manifoldID = request.args.get('manifoldID')
        channelID = request.args.get('channelID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        noCL = request.args.get('noCL')
        starttime = addSingleQuote(starttime)
        endtime = addSingleQuote(endtime)
        print("MACHINEID:", machineID)
        print("starttime:", starttime)
        print("endtime:", endtime)
        statusCode, paramList, dateList = mouldfloapi.mouldflo_historical(machineID, manifoldID, channelID, fieldID,
                                                                          starttime,
                                                                          endtime)
        if (statusCode == 200):
            print('status-code: ', statusCode)
            return render_template('histoHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   title=title,
                                   ylabel=ylabel,
                                   envparameter=envparameter
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "motan":
        print("INSIDE  HISTOGRAM MOTAN-HISTORICAL")
        machineID = request.args.get('machineID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        noCL = request.args.get('noCL')
        starttime = addSingleQuote(starttime)
        endtime = addSingleQuote(endtime)
        print("MACHINEID:", machineID)
        print("starttime:", starttime)
        print("endtime:", endtime)
        statusCode, paramList, dateList = motanapi.motan_historical(machineID, fieldID, starttime, endtime)
        if (statusCode == 200):
            print('status-code: ', statusCode)
            return render_template('histoHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   title=title,
                                   ylabel=ylabel,
                                   envparameter=envparameter
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "conair":
        print("INSIDE HISTOGRAM CONAIR-HISTORICAL")
        machineID = request.args.get('machineID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        noCL = request.args.get('noCL')
        starttime = addSingleQuote(starttime)
        endtime = addSingleQuote(endtime)
        print("MACHINEID:", machineID)
        print("starttime:", starttime)
        print("endtime:", endtime)
        statusCode, paramList, dateList = conairapi.conair_historical(machineID, fieldID, starttime, endtime)
        if (statusCode == 200):
            print('status-code: ', statusCode)
            return render_template('histoHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   title=title,
                                   ylabel=ylabel,
                                   envparameter=envparameter
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "cda":
        print("INSIDE  HISTOGRAM CDA-HISTORICAL")
        cdaID = request.args.get('cdaID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        noCL = request.args.get('noCL')
        starttime = addSingleQuote(starttime)
        endtime = addSingleQuote(endtime)
        print("starttime:", starttime)
        print("endtime:", endtime)
        statusCode, paramList, dateList = cdaapi.cda_historical(cdaID, fieldID, starttime, endtime)
        if (statusCode == 200):
            print('status-code: ', statusCode)
            return render_template('histoHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   title=title,
                                   ylabel=ylabel,
                                   envparameter=envparameter
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
        return 0

'''
╦  ╦╦  ╦╔═╗
║  ║╚╗╔╝║╣ 
╩═╝╩ ╚╝ ╚═╝
'''

@histoApp.route("/live/<machinename>")
def histoLive(machinename):
    # parameters
    duration = request.args.get('duration')
    xlabel = request.args.get('xlabel')
    ylabel = request.args.get('ylabel')
    title = request.args.get('title')
    lcl = request.args.get('lcl')
    ucl = request.args.get('ucl')
    sp = request.args.get('sp')
    freq = request.args.get('freq')
    if machinename == "envdata":
        print("INSIDE HISTO ENV-DATA LIVE")
        envparameter = request.args.get('envparameter')  # humidity or temperature
        statusCode, tempList, humList, dateList = externalrestapiApp.env_live(int(duration))
        if envparameter == "temperature":
            if (statusCode == 200):
                return render_template('histoLive.html',
                                       dateTime=dateList,
                                       plotParameter=tempList,
                                       title=title,
                                       ylabel=ylabel,
                                       freq=freq,
                                       lcl=lcl,
                                       ucl=ucl,
                                       sp=sp,
                                       envparameter=envparameter,
                                       machinename=machinename,
                                       duration=duration,
                                       )
            elif (statusCode == 999):
                return render_template('ConnectionError.html')
            else:
                return render_template('tableNotFound.html')
        elif envparameter == "humidity":
            if (statusCode == 200):
                return render_template('histoLive.html',
                                       dateTime=dateList,
                                       plotParameter=humList,
                                       title=title,
                                       ylabel=ylabel,
                                       freq=freq,
                                       lcl=lcl,
                                       ucl=ucl,
                                       sp=sp,
                                       envparameter=envparameter,
                                       machinename=machinename,
                                       duration=duration,
                                       )
            elif (statusCode == 999):
                return render_template('ConnectionError.html')
            else:
                return render_template('tableNotFound.html')
    if machinename == "fanuc":
        machineID = request.args.get('machineID')
        paraIndex = request.args.get('paraIndex')
        envparameter = request.args.get('envparameter')
        statusCode, paramList, dateList = externalrestapiApp.fanuc_live(machineID, paraIndex, int(duration))
        if (statusCode == 200):
            return render_template('histoLive.html',
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
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "moldmaster":
        print("INSIDE MOLDMASTERLIVE")
        machineID = request.args.get('machineID')
        tipID = request.args.get('tipID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = moldmasterapi.moldmaster_live(machineID, tipID, fieldID, duration)
        if (statusCode == 200):
            print('status-code:', statusCode)
            return render_template('histoLive.html',
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
                                   tipID=tipID,
                                   fieldID=fieldID,
                                   duration=duration,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "mouldflo":
        print("INSIDE HISTOGRAM-MOULDFLO-LIVE")
        machineID = request.args.get('machineID')
        manifoldID = request.args.get('manifoldID')
        channelID = request.args.get('channelID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = mouldfloapi.mouldflo_live(machineID, manifoldID, channelID, fieldID, duration)
        if (statusCode == 200):
            print('status-code:', statusCode)
            return render_template('histoLive.html',
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
                                   manifoldID=manifoldID,
                                   channelID=channelID,
                                   fieldID=fieldID,
                                   duration=duration,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "motan":
        print("INSIDE HISTOGRAM-MOTAN-LIVE")
        machineID = request.args.get('machineID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = motanapi.motan_live(machineID, fieldID, duration)
        if (statusCode == 200):
            print('status-code:', statusCode)
            return render_template('histoLive.html',
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
                                   fieldID=fieldID,
                                   duration=duration,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
        return 0
    elif machinename == "conair":
        print("INSIDE HISTOGRAM-CONAIR-LIVE")
        machineID = request.args.get('machineID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = conairapi.conair_live(machineID, fieldID, duration)
        if (statusCode == 200):
            print('status-code:', statusCode)
            return render_template('histoLive.html',
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
                                   fieldID=fieldID,
                                   duration=duration,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
        return 0
    elif machinename == "cda":
        print("INSIDE HISTOGRAM-CDA-LIVE")
        cdaID = request.args.get('cdaID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = cdaapi.cda_live(cdaID, fieldID, duration)
        if (statusCode == 200):
            print('status-code:', statusCode)
            return render_template('histoLive.html',
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
                                   cdaID=cdaID,
                                   fieldID=fieldID,
                                   duration=duration,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')

@histoApp.route("/<machinename>")
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
        return render_template('histoTorquePowerLastHour.html', response=mystring, title=title, freq=freq)
    if (machinename == 'testcsv'):
        dateTime, readValue, upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')
        print(readValue)
        print("x:", dateTime[0])
        return render_template('histopage.html', readValue=readValue)
    elif (machinename == 'fanuc'):
        dateTime, readTorque, readPower, torqueStdDev, powerStdDev, torqueMean, powerMean,xList, yList = readTorquePower('fanuc-torque-power.csv')
        print("torquestddev: ", torqueStdDev)
        print("powerstddev: ", powerStdDev )
        print("torquemean: ", torqueMean)
        print("powermean: ", powerMean)
        return render_template('histoTorquePower.html', dateTime=dateTime, readTorque=readTorque, readPower=readPower, torqueStdDev=torqueStdDev, powerStdDev=powerStdDev, torqueMean=torqueMean, powerMean=powerMean, title=title, titlex=titlex, titley=titley,xList=xList, yList=yList, starttime=starttime, endtime=endtime)
    else:
        return render_template('tableNotFound.html')

@histoApp.route("/duration/<machinename>")
def duration(machinename):
    lasthours = request.args.get('lasthours')
    freq = request.args.get('freq')
    title = request.args.get('title')
    if (lasthours and freq):
        resp = restdatageneratorApp.default()
        mystring = resp.response
        return render_template('histoTorquePowerLastHour.html', response=mystring, title=title, freq=freq)
    else:
        return "BAD: lasthours arguement is not specified"
@histoApp.route("/timerange/<machinename>")
def timerange(machinename):
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    title = request.args.get('title')
    freq = request.args.get('freq')
    if (starttime and endtime):
        return "Good"
    else:
        return "Bad"