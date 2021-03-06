from flask import Flask, render_template
from util import readCsvFile
from box.boxApp import boxApp
from line.lineApp import lineApp
from histogram.histoApp import histoApp
from base.baseApp import baseApp
from spc.spcApp import spcApp
from restdatagenerator.restdatageneratorApp import restdatageneratorApp
from waitress import serve

app = Flask(__name__)
app.secret_key = "dev"
app.register_blueprint(boxApp, url_prefix="/box")
app.register_blueprint(lineApp, url_prefix="/line")
app.register_blueprint(histoApp, url_prefix="/histogram")
app.register_blueprint(baseApp, url_prefix="/base")
app.register_blueprint(spcApp, url_prefix="/spc")
app.register_blueprint(restdatageneratorApp,url_prefix="/restdatagenerator")

@app.route('/')
def default():
    dateTime, readValue,upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')
    print (readValue)
    print ("x:",dateTime[0])
    return render_template('iframe.html')


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)
    serve(app, host='0.0.0.0', port=5000)
