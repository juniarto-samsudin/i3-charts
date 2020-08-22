from flask import Flask, render_template
from util import readCsvFile
from box.boxApp import boxApp
from line.lineApp import lineApp
from histogram.histoApp import histoApp

app = Flask(__name__)
app.secret_key = "dev"
app.register_blueprint(boxApp, url_prefix="/box")
app.register_blueprint(lineApp, url_prefix="/line")
app.register_blueprint(histoApp, url_prefix="/histogram")

@app.route('/')
def default():
    dateTime, readValue,upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')
    print (readValue)
    print ("x:",dateTime[0])
    return render_template('line/templates/time-series.html', dateTime=dateTime, readValue=readValue, upperLimit=upperLimit, lowerLimit=lowerLimit, setPoint=setPoint)


if __name__ == '__main__':
    app.run()
