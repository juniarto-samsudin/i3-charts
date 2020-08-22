from flask import Flask, render_template
from util import readCsvFile

app = Flask(__name__)


@app.route('/')
def default():
    dateTime, readValue,upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')
    print (readValue)
    print ("x:",dateTime[0])
    return render_template('time-series.html', dateTime=dateTime, readValue=readValue, upperLimit=upperLimit, lowerLimit=lowerLimit, setPoint=setPoint)


if __name__ == '__main__':
    app.run()
