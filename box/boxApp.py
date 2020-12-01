from flask import Blueprint, render_template, request
from box.util import readCsvFile, addSingleQuote
from restdatagenerator import restdatageneratorApp
from externalrestapi import externalrestapiApp, moldmasterapi, mouldfloapi, motanapi, conairapi, cdaapi

boxApp = Blueprint("boxApplication", __name__, static_folder="static", template_folder="templates")

'''
╦ ╦╦╔═╗╔╦╗╔═╗╦═╗╦╔═╗╔═╗╦  
╠═╣║╚═╗ ║ ║ ║╠╦╝║║  ╠═╣║  
╩ ╩╩╚═╝ ╩ ╚═╝╩╚═╩╚═╝╩ ╩╩═╝
'''
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
        statusCode,paramList, dateList = externalrestapiApp.fanuc_historical(int(machineID), int(paraIndex), str(starttime),
                                                                  str(endtime))
        if (statusCode == 200):
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
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "moldmaster":
        print("INSIDE BOX MOLDMASTER HISTORICAL ")
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
            return render_template('boxHistorical.html',
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
        print("INSIDE  BOX MOULDFLO-HISTORICAL")
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
            return render_template('boxHistorical.html',
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
        print("INSIDE  BOX MOTAN-HISTORICAL")
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
            return render_template('boxHistorical.html',
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
        print("INSIDE BOX CONAIR-HISTORICAL")
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
            return render_template('boxHistorical.html',
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
        print("INSIDE  BOX CDA-HISTORICAL")
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
            return render_template('boxHistorical.html',
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

'''
╦  ╦╦  ╦╔═╗
║  ║╚╗╔╝║╣ 
╩═╝╩ ╚╝ ╚═╝
'''
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
        statusCode, paramList, dateList = externalrestapiApp.fanuc_live(machineID, paraIndex, int(duration))
        if (statusCode == 200):
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
        print("INSIDE BOX-MOULDFLO-LIVE")
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
        print("INSIDE BOX-MOTAN-LIVE")
        machineID = request.args.get('machineID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = motanapi.motan_live(machineID, fieldID, duration)
        if (statusCode == 200):
            print('status-code:', statusCode)
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
                                   fieldID=fieldID,
                                   duration=duration,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "conair":
        print("INSIDE BOX-CONAIR-LIVE")
        machineID = request.args.get('machineID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = conairapi.conair_live(machineID, fieldID, duration)
        if (statusCode == 200):
            print('status-code:', statusCode)
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
                                   fieldID=fieldID,
                                   duration=duration,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "cda":
        print("INSIDE BOX-CDA-LIVE")
        cdaID = request.args.get('cdaID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = cdaapi.cda_live(cdaID, fieldID, duration)
        if (statusCode == 200):
            print('status-code:', statusCode)
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
                                   cdaID=cdaID,
                                   fieldID=fieldID,
                                   duration=duration,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')

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