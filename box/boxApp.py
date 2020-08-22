from flask import Blueprint, render_template
from util import readCsvFile

boxApp = Blueprint("boxApp", __name__, static_folder="static", template_folder="templates")

@boxApp.route("/")
def default():
    dateTime, readValue, upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')

    return render_template("boxpage.html", readValue=readValue)