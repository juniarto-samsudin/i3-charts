from flask import Blueprint, render_template, request, url_for
from line.util import readCsvFile, readTorquePower, addSingleQuote
import requests
from restdatagenerator import restdatageneratorApp
from externalrestapi import externalrestapiApp, moldmasterapi, mouldfloapi, motanapi, conairapi, cdaapi, predapi
import simplejson as json

lineApp = Blueprint("lineApplication", __name__, static_folder="static", template_folder="templates")

'''
╦ ╦╦╔═╗╔╦╗╔═╗╦═╗╦╔═╗╔═╗╦  
╠═╣║╚═╗ ║ ║ ║╠╦╝║║  ╠═╣║  
╩ ╩╩╚═╝ ╩ ╚═╝╩╚═╩╚═╝╩ ╩╩═╝
'''
@lineApp.route("/historical/<machinename>")
def lineHistorical(machinename):
    #parameters
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    xlabel = request.args.get('xlabel')
    ylabel = request.args.get('ylabel')
    title = request.args.get('title')
    lcl = request.args.get('lcl')
    ucl = request.args.get('ucl')
    sp = request.args.get('sp')
    if machinename == "envdata":
        print("INSIDE ENVDATA LINE HISTORICAL")
        envparameter = request.args.get('envparameter')  # humidity or temperature
        noCL = request.args.get('noCL')
        statusCode, tempList, humList, dateList = externalrestapiApp.env_historical(starttime, endtime)
        if (statusCode == 200):
            if envparameter == "temperature":
                return render_template('lineHistorical.html',
                                       dateTime=dateList,
                                       plotParameter=tempList,
                                       lcl=int(lcl),
                                       ucl=int(ucl),
                                       sp=int(sp),
                                       title=title,
                                       ylabel=ylabel,
                                       envparameter=envparameter,
                                       noCL=noCL
                                       )
            elif envparameter == "humidity":
                return render_template('lineHistorical.html',
                                       dateTime=dateList,
                                       plotParameter=humList,
                                       lcl=int(lcl),
                                       ucl=int(ucl),
                                       sp=int(sp),
                                       title=title,
                                       ylabel=ylabel,
                                       envparameter=envparameter,
                                       noCL=noCL
                                       )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "fanuc":
        machineID = request.args.get('machineID')
        paraIndex = request.args.get('paraIndex')
        envparameter = request.args.get('envparameter')
        noCL = request.args.get('noCL')
        starttime = addSingleQuote(starttime)
        endtime = addSingleQuote(endtime)
        print("MACHINEID:", machineID)
        print("paraIndex:", paraIndex)
        print("starttime:", starttime)
        print("endtime:", endtime)
        statusCode,paramList, dateList = externalrestapiApp.fanuc_historical(int(machineID), int(paraIndex), str(starttime),
                                                                  str(endtime))
        if (statusCode == 200):
            return render_template('lineHistorical.html',
                               dateTime=dateList,
                               plotParameter=paramList,
                               lcl=int(lcl),
                               ucl=int(ucl),
                               sp=int(sp),
                               title=title,
                               ylabel=ylabel,
                               envparameter=envparameter,
                               noCL=noCL
                               )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')

    elif machinename == "moldmaster":
        print("INSIDE LINE MOLDMASTERHISTORICAL")
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
            return render_template('lineHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   lcl=lcl,
                                   ucl=ucl,
                                   sp=sp,
                                   title=title,
                                   ylabel=ylabel,
                                   envparameter=envparameter,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "mouldflo":
        print("INSIDE MOULDFLO-HISTORICAL")
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
            return render_template('lineHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   lcl=lcl,
                                   ucl=ucl,
                                   sp=sp,
                                   title=title,
                                   ylabel=ylabel,
                                   envparameter=envparameter,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "motan":
        print("INSIDE MOTAN-HISTORICAL")
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
            return render_template('lineHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   lcl=lcl,
                                   ucl=ucl,
                                   sp=sp,
                                   title=title,
                                   ylabel=ylabel,
                                   envparameter=envparameter,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "conair":
        print("INSIDE CONAIR-HISTORICAL")
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
            return render_template('lineHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   lcl=lcl,
                                   ucl=ucl,
                                   sp=sp,
                                   title=title,
                                   ylabel=ylabel,
                                   envparameter=envparameter,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "cda":
        print("INSIDE CDA-HISTORICAL")
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
            return render_template('lineHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   lcl=lcl,
                                   ucl=ucl,
                                   sp=sp,
                                   title=title,
                                   ylabel=ylabel,
                                   envparameter=envparameter,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "predict":
        print("INSIDE LINE-PREDICT-HISTORICAL")
        machineID = request.args.get('machineID')
        #fieldID = request.args.get('fieldID')
        fieldID = 0
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = predapi.pred_historical(machineID, starttime, endtime)
        if (statusCode == 200):
            print('status-code:', statusCode)
            return render_template('lineHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   title=title,
                                   ylabel=ylabel,
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

'''
╦  ╦╦  ╦╔═╗
║  ║╚╗╔╝║╣ 
╩═╝╩ ╚╝ ╚═╝
'''

@lineApp.route("/live/<machinename>")
def lineLive(machinename):
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
        print("INSIDE LINE ENV-DATA LIVE")
        envparameter = request.args.get('envparameter')  # humidity or temperature
        noCL = request.args.get('noCL')
        statusCode, tempList, humList, dateList = externalrestapiApp.env_live(int(duration))
        if envparameter == "temperature":
            if (statusCode == 200):
                return render_template('lineLive.html',
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
                                       noCL=noCL)
            elif (statusCode == 999):
                return render_template('ConnectionError.html')
            else:
                return render_template('tableNotFound.html')
        elif envparameter == "humidity":
            if (statusCode == 200):
                return render_template('lineLive.html',
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
                                       noCL=noCL)
            elif (statusCode == 999):
                return render_template('ConnectionError.html')
            else:
                return render_template('tableNotFound.html')
    elif machinename == "fanuc":
        machineID = request.args.get('machineID')
        paraIndex = request.args.get('paraIndex')
        envparameter = request.args.get('envparameter')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = externalrestapiApp.fanuc_live(machineID, paraIndex, int(duration))
        if (statusCode == 200):
            return render_template('lineLive.html',
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
                               duration=duration,
                               noCL = noCL
                               )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "moldmaster":
        print("INSIDE LINE LIVE MOLDMASTER")
        machineID = request.args.get('machineID')
        tipID = request.args.get('tipID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = moldmasterapi.moldmaster_live(machineID, tipID, fieldID, duration)
        if (statusCode == 200):
            print('status-code:', statusCode)
            return render_template('lineLive.html',
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
                                   duration=duration,
                                   tipID=tipID,
                                   fieldID=fieldID,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "mouldflo":
        print("INSIDE LINE-MOULDFLO-LIVE")
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
            return render_template('lineLive.html',
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
        print("INSIDE LINE-MOTAN-LIVE")
        machineID = request.args.get('machineID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = motanapi.motan_live(machineID, fieldID, duration)
        if (statusCode == 200):
            print('status-code:', statusCode)
            return render_template('lineLive.html',
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
    elif machinename == "conair":
        print("INSIDE LINE-CONAIR-LIVE")
        machineID = request.args.get('machineID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = conairapi.conair_live(machineID, fieldID, duration)
        if (statusCode == 200):
            print('status-code:', statusCode)
            return render_template('lineLive.html',
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
    elif machinename == "cda":
        print("INSIDE LINE-CDA-LIVE")
        cdaID = request.args.get('cdaID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = cdaapi.cda_live(cdaID, fieldID, duration)
        if (statusCode == 200):
            print('status-code:', statusCode)
            return render_template('lineLive.html',
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
    elif machinename == "predict":
        print("INSIDE LINE-PREDICT-LIVE")
        machineID = request.args.get('machineID')
        #fieldID = request.args.get('fieldID')
        fieldID = 0
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = predapi.pred_live(machineID, duration)
        if (statusCode == 200):
            print('status-code:', statusCode)
            return render_template('lineLive.html',
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

