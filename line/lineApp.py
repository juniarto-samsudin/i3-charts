from flask import Blueprint, render_template
from util import readCsvFile

lineApp = Blueprint("lineApplication", __name__, static_folder="static", template_folder="templates")

@lineApp.route("/")
def default():
    dateTime, readValue, upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')
    print(readValue)
    print("x:", dateTime[0])
    return render_template('linepage.html', dateTime=dateTime, readValue=readValue, upperLimit=upperLimit,
                           lowerLimit=lowerLimit, setPoint=setPoint)
