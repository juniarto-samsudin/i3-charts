from flask import Blueprint, render_template, request
from util import readCsvFile

lineApp = Blueprint("lineApplication", __name__, static_folder="static", template_folder="templates")

@lineApp.route("/<table>")
def default(table):
    user = request.args.get('user')
    print("USER: ", user)
    if (table == 'testcsv'):
        dateTime, readValue, upperLimit, lowerLimit, setPoint = readCsvFile('temperature.csv')
        print(readValue)
        print("x:", dateTime[0])
        return render_template('linepage.html', dateTime=dateTime, readValue=readValue, upperLimit=upperLimit,
                           lowerLimit=lowerLimit, setPoint=setPoint)
    else:
        return render_template('tableNotFound.html')

