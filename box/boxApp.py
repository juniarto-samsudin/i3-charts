from flask import Blueprint, render_template
from util import readCsvFile

boxApp = Blueprint("boxApplication", __name__, static_folder="static", template_folder="templates")

@boxApp.route("/<table>")
def default(table):
    if (table == "testcsv"):
        dateTime, readValue, upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')
        return render_template("boxpage.html", readValue=readValue)
    else:
        return render_template('tableNotFound.html')