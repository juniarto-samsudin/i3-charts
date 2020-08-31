from flask import Blueprint, render_template
from util import readCsvFile

histoApp = Blueprint("histoApplication", __name__, static_folder="static", template_folder="templates")

@histoApp.route("/<table>")
def default(table):
    if (table == 'testcsv'):
        dateTime, readValue, upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')
        print(readValue)
        print("x:", dateTime[0])
        return render_template('histopage.html', readValue=readValue)
    else:
        return render_template('tableNotFound.html')