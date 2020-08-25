from flask import Blueprint, render_template, request
from util import readCsvFile

spcApp = Blueprint("spcApplication", __name__, static_folder="static", template_folder="templates")

@spcApp.route("/<table>")
def default(table):
    if (table == "testcsv"):
        dateTime, readValue, upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')
        return render_template('spcpage.html', dateTime=dateTime, readValue=readValue, upperLimit=upperLimit,
                               lowerLimit=lowerLimit, setPoint=setPoint)
    else:
        return render_template('tableNotFound.html')