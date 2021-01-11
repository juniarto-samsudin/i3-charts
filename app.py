from flask import Flask, render_template
from util import readCsvFile
from box.boxApp import boxApp
from line.lineApp import lineApp
from histogram.histoApp import histoApp
from base.baseApp import baseApp
from spc.spcApp import spcApp
from restdatagenerator.restdatageneratorApp import restdatageneratorApp
from externalrestapi.externalrestapiApp import externalrestapiApp
from externalrestapi.moldmasterapi import moldmasterapiApp
from externalrestapi.mouldfloapi import mouldfloapiApp
from externalrestapi.motanapi import motanapiApp
from externalrestapi.conairapi import conairapiApp
from externalrestapi.cdaapi import cdaapiApp

app = Flask(__name__)
app.secret_key = "dev"
app.register_blueprint(boxApp, url_prefix="/box")
app.register_blueprint(lineApp, url_prefix="/line")
app.register_blueprint(histoApp, url_prefix="/histogram")
app.register_blueprint(baseApp, url_prefix="/base")
app.register_blueprint(spcApp, url_prefix="/spc")
app.register_blueprint(restdatageneratorApp,url_prefix="/restdatagenerator")
app.register_blueprint(externalrestapiApp,url_prefix="/externalrestapi")
app.register_blueprint(moldmasterapiApp,url_prefix="/moldmasterapi")
app.register_blueprint(mouldfloapiApp,url_prefix="/mouldfloapi")
app.register_blueprint(motanapiApp,url_prefix="/motanapi")
app.register_blueprint(conairapiApp,url_prefix="/conairapi")
app.register_blueprint(cdaapiApp, url_prefix="/cdaapi")

try:
    #GET FROM EXTERNAL ENV VARIABLE SETTINGS
    print("USING ENVIRONMENT VARIABLE")
    app.config.from_envvar('MYAPPLICATIONSETTING')
except:
    #FALL BACK USING config.py
    print("USING CONFIG.PY")
    app.config.from_object("config.ProductionConfig")

@app.route('/')
def default():
    dateTime, readValue,upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')
    #print (readValue)
    #print ("x:",dateTime[0])
    return render_template('iframe.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
