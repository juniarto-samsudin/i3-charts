from flask import Blueprint, render_template
from util import readCsvFile

histoApp = Blueprint("histoApplication", __name__, static_folder="static", template_folder="templates")

@histoApp.route("/")
def default():
    dateTime, readValue, upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')
    print(readValue)
    print("x:", dateTime[0])
    return render_template('histopage.html', readValue=readValue)