from flask import Blueprint, render_template, request
from spc.util import readCsvFile, readTorquePower, getStatisticFromList, addSingleQuote
from restdatagenerator import restdatageneratorApp
from externalrestapi import externalrestapiApp, moldmasterapi, mouldfloapi, motanapi, conairapi, cdaapi, predapi

spcApp = Blueprint("spcApplication", __name__, static_folder="static", template_folder="templates")

'''
╦ ╦╦╔═╗╔╦╗╔═╗╦═╗╦╔═╗╔═╗╦  
╠═╣║╚═╗ ║ ║ ║╠╦╝║║  ╠═╣║  
╩ ╩╩╚═╝ ╩ ╚═╝╩╚═╩╚═╝╩ ╩╩═╝
'''

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

    if machinename == "envdata":
        #print("INSIDE ENVDATA SPC HISTORICAL")
        envparameter = request.args.get('envparameter') #humidity or temperature
        noCL = request.args.get('noCL')
        statusCode, tempList, humList, dateList = externalrestapiApp.env_historical(starttime, endtime)
        if (statusCode == 200):
            if envparameter == "temperature":
                if len(tempList) == 0:
                    return render_template('DataNotFound.html')
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
                                    envparameter = envparameter,
                                    noCL = noCL
                                   )
            elif envparameter == "humidity":
                if len(humList) == 0:
                    return render_template('DataNotFound.html')
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
                                   envparameter=envparameter,
                                   noCL = noCL
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
        #print("MACHINEID:", machineID)
        #print("paraIndex:", paraIndex)
        #print("starttime:", starttime)
        #print("endtime:", endtime)
        statusCode, paramList, dateList = externalrestapiApp.fanuc_historical(int(machineID), int(paraIndex), str(starttime), str(endtime))
        #StdDev, Mean, xNormDistList, yNormDistList = getStatisticFromList(paramList)
        if (statusCode == 200):
            if len(paramList) == 0:
                return render_template('DataNotFound.html')
            StdDev, Mean, xNormDistList, yNormDistList = getStatisticFromList(paramList)
            return render_template('spcHistorical.html',
                               dateTime=dateList,
                               plotParameter=paramList,
                               StdDev=StdDev,
                               lcl=int(lcl),
                               ucl=int(ucl),
                               sp=int(sp),
                               title=title,
                               ylabel=ylabel,
                               xNormalDistList=xNormDistList,
                               yNormalDistList=yNormDistList,
                               envparameter=envparameter,
                               noCL = noCL
                               )
        elif(statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "moldmaster":
        #print("INSIDE MOLDMASTERHISTORICAL")
        machineID = request.args.get('machineID')
        tipID = request.args.get('tipID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        noCL = request.args.get('noCL')
        starttime = addSingleQuote(starttime)
        endtime = addSingleQuote(endtime)
        #print("MACHINEID:", machineID)
        #print("starttime:", starttime)
        #print("endtime:", endtime)
        statusCode, paramList, dateList = moldmasterapi.moldmaster_historical(machineID, tipID, fieldID, starttime, endtime)
        if (statusCode == 200):
            #print('status-code: ', statusCode)
            if len(paramList) == 0:
                return render_template('DataNotFound.html')
            StdDev, Mean, xNormDistList, yNormDistList = getStatisticFromList(paramList)
            #print('after statistics')
            return render_template('spcHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   StdDev=StdDev,
                                   lcl=lcl,
                                   ucl=ucl,
                                   sp=sp,
                                   title=title,
                                   ylabel=ylabel,
                                   xNormalDistList=xNormDistList,
                                   yNormalDistList=yNormDistList,
                                   envparameter=envparameter,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "mouldflo":
        #print("INSIDE MOULDFLO-HISTORICAL")
        machineID = request.args.get('machineID')
        manifoldID = request.args.get('manifoldID')
        channelID = request.args.get('channelID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        noCL = request.args.get('noCL')
        starttime = addSingleQuote(starttime)
        endtime = addSingleQuote(endtime)
        #print("MACHINEID:", machineID)
        #print("starttime:", starttime)
        #print("endtime:", endtime)
        statusCode, paramList, dateList = mouldfloapi.mouldflo_historical(machineID, manifoldID, channelID, fieldID, starttime,
                                                                              endtime)
        if (statusCode == 200):
            #print('status-code: ', statusCode)
            if len(paramList) == 0:
                return render_template('DataNotFound.html')
            StdDev, Mean, xNormDistList, yNormDistList = getStatisticFromList(paramList)
            #print('after statistics')
            return render_template('spcHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   StdDev=StdDev,
                                   lcl=lcl,
                                   ucl=ucl,
                                   sp=sp,
                                   title=title,
                                   ylabel=ylabel,
                                   xNormalDistList=xNormDistList,
                                   yNormalDistList=yNormDistList,
                                   envparameter=envparameter,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "motan":
        #print("INSIDE MOTAN-HISTORICAL")
        machineID = request.args.get('machineID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        noCL = request.args.get('noCL')
        starttime = addSingleQuote(starttime)
        endtime = addSingleQuote(endtime)
        #print("MACHINEID:", machineID)
        #print("starttime:", starttime)
        #print("endtime:", endtime)
        statusCode, paramList, dateList = motanapi.motan_historical(machineID,fieldID,starttime,endtime)
        if (statusCode == 200):
            #print('status-code: ', statusCode)
            if len(paramList) == 0:
                return render_template('DataNotFound.html')
            StdDev, Mean, xNormDistList, yNormDistList = getStatisticFromList(paramList)
            #print('after statistics')
            return render_template('spcHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   StdDev=StdDev,
                                   lcl=lcl,
                                   ucl=ucl,
                                   sp=sp,
                                   title=title,
                                   ylabel=ylabel,
                                   xNormalDistList=xNormDistList,
                                   yNormalDistList=yNormDistList,
                                   envparameter=envparameter,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "conair":
        #print("INSIDE CONAIR-HISTORICAL")
        machineID = request.args.get('machineID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        noCL = request.args.get('noCL')
        starttime = addSingleQuote(starttime)
        endtime = addSingleQuote(endtime)
        #print("MACHINEID:", machineID)
        #print("starttime:", starttime)
        #print("endtime:", endtime)
        statusCode, paramList, dateList = conairapi.conair_historical(machineID, fieldID, starttime, endtime)
        if (statusCode == 200):
            #print('status-code: ', statusCode)
            if len(paramList) == 0:
                return render_template('DataNotFound.html')
            StdDev, Mean, xNormDistList, yNormDistList = getStatisticFromList(paramList)
            #print('after statistics')
            return render_template('spcHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   StdDev=StdDev,
                                   lcl=lcl,
                                   ucl=ucl,
                                   sp=sp,
                                   title=title,
                                   ylabel=ylabel,
                                   xNormalDistList=xNormDistList,
                                   yNormalDistList=yNormDistList,
                                   envparameter=envparameter,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "cda":
        #print("INSIDE CDA-HISTORICAL")
        cdaID = request.args.get('cdaID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        noCL = request.args.get('noCL')
        starttime = addSingleQuote(starttime)
        endtime = addSingleQuote(endtime)
        #print("starttime:", starttime)
        #print("endtime:", endtime)
        statusCode, paramList, dateList = cdaapi.cda_historical(cdaID, fieldID, starttime, endtime)
        if (statusCode == 200):
            #print('status-code: ', statusCode)
            if len(paramList) == 0:
                return render_template('DataNotFound.html')
            StdDev, Mean, xNormDistList, yNormDistList = getStatisticFromList(paramList)
            #print('after statistics')
            return render_template('spcHistorical.html',
                                   dateTime=dateList,
                                   plotParameter=paramList,
                                   StdDev=StdDev,
                                   lcl=lcl,
                                   ucl=ucl,
                                   sp=sp,
                                   title=title,
                                   ylabel=ylabel,
                                   xNormalDistList=xNormDistList,
                                   yNormalDistList=yNormDistList,
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
@spcApp.route("/live/<machinename>")
def spcLive(machinename):
    print("SPC-LIVE")
    #parameters
    duration = request.args.get('duration')
    xlabel = request.args.get('xlabel')
    ylabel = request.args.get('ylabel')
    title = request.args.get('title')
    lcl = request.args.get('lcl')
    ucl = request.args.get('ucl')
    sp = request.args.get('sp')
    freq = request.args.get('freq')
    #get-data
    if machinename == "envdata":
        #print("LIVE-ENVDATA")
        envparameter = request.args.get('envparameter')  # humidity or temperature
        noCL = request.args.get('noCL')
        statusCode, tempList, humList, dateList = externalrestapiApp.env_live(int(duration))
        if envparameter == "temperature":
            if (statusCode == 200):
                return render_template('spcLive.html',
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
                                   noCL = noCL    )
            elif(statusCode == 999):
                return render_template('ConnectionError.html')
            else:
                return render_template('tableNotFound.html')
        elif envparameter == "humidity":
            if (statusCode == 200):
                return render_template('spcLive.html',
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
                                   noCL = noCL    )
            elif(statusCode == 999):
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
            return render_template('spcLive.html',
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
        #print("INSIDE MOLDMASTERLIVE")
        machineID = request.args.get('machineID')
        tipID = request.args.get('tipID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = moldmasterapi.moldmaster_live(machineID, tipID, fieldID, duration)
        if (statusCode == 200):
            #print('status-code:', statusCode)
            return render_template('spcLive.html',
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
                                   tipID = tipID,
                                   fieldID = fieldID,
                                   duration=duration,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "mouldflo":
        #print("INSIDE MOULDFLO-LIVE")
        machineID = request.args.get('machineID')
        manifoldID = request.args.get('manifoldID')
        channelID = request.args.get('channelID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = mouldfloapi.mouldflo_live(machineID, manifoldID, channelID, fieldID, duration)
        if (statusCode == 200):
            #print('status-code:', statusCode)
            return render_template('spcLive.html',
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
        #print("INSIDE MOTAN-LIVE")
        machineID = request.args.get('machineID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = motanapi.motan_live(machineID, fieldID, duration)
        if (statusCode == 200):
            #print('status-code:', statusCode)
            return render_template('spcLive.html',
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
        #print("INSIDE CONAIR-LIVE")
        machineID = request.args.get('machineID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = conairapi.conair_live(machineID, fieldID, duration)
        if (statusCode == 200):
            #print('status-code:', statusCode)
            return render_template('spcLive.html',
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
        #print("INSIDE CDA-LIVE")
        cdaID = request.args.get('cdaID')
        fieldID = request.args.get('fieldID')
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList = cdaapi.cda_live(cdaID, fieldID, duration)
        if (statusCode == 200):
            #print('status-code:', statusCode)
            return render_template('spcLive.html',
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
                                   cdaID = cdaID,
                                   fieldID=fieldID,
                                   duration=duration,
                                   noCL=noCL
                                   )
        elif (statusCode == 999):
            return render_template('ConnectionError.html')
        else:
            return render_template('tableNotFound.html')
    elif machinename == "predict":
        print("INSIDE SPCAPP-PRED-LIVE")
        print("MACHINE_NAME: ", machinename)
        machineID = request.args.get('machineID')
        #fieldID = request.args.get('fieldID')
        fieldID = 0
        envparameter = request.args.get('envparameter')
        duration = request.args.get('duration')
        noCL = request.args.get('noCL')
        statusCode, paramList, dateList =  predapi.pred_live(machineID, duration)
        if (statusCode == 200):
            print('status-code:', statusCode)
            return render_template('spcLive.html',
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

@spcApp.route("/<machinename>")
def default(machinename):
    #print(request.query_string.decode('utf-8'))
    parameters = request.args.getlist("parameters")
    #print("PARAMETERS: ", parameters)
    # example: http://127.0.0.1:5000/line/fanuc?title=juniarto&parameters=temperature&parameters=pressure&parameters=torque
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    title = request.args.get('title')
    lasthours = request.args.get('lasthours')
    freq = request.args.get('freq')
    titlex = request.args.get('titlex')
    titley = request.args.get('titley')
    #print("STARTIME: ", starttime)
    #print("ENDTIME: ", endtime)
    #print("TITLE:", title)
    #print("FREQ:", freq)
    if (lasthours):
        #print("LASTHOURS: ", lasthours)
        resp = restdatageneratorApp.default() #RESPONSE OBJECT
        mystring = resp.response #STRING
        return render_template('spcTorquePowerLastHour.html', response=mystring, title=title, freq=freq)
    if (machinename == "testcsv"):
        dateTime, readValue, upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')
        return render_template('spcpage.html', dateTime=dateTime, readValue=readValue, upperLimit=upperLimit,
                               lowerLimit=lowerLimit, setPoint=setPoint)
    elif (machinename == 'fanuc'):
        dateTime, readTorque, readPower, torqueStdDev, powerStdDev, torqueMean, powerMean,xList, yList = readTorquePower('fanuc-torque-power.csv')
        #print("torquestddev: ", torqueStdDev)
        #print("powerstddev: ", powerStdDev )
        #print("torquemean: ", torqueMean)
        #print("powermean: ", powerMean)
        return render_template('spcTorquePower.html', dateTime=dateTime, readTorque=readTorque, readPower=readPower, torqueStdDev=torqueStdDev, powerStdDev=powerStdDev, torqueMean=torqueMean, powerMean=powerMean, title=title, titlex=titlex, titley=titley,xList=xList, yList=yList, starttime=starttime, endtime=endtime)
    else:
        return render_template('tableNotFound.html')
