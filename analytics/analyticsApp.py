from flask import Blueprint, render_template, request

analyticsApp = Blueprint("analyticsApplication", __name__, static_folder="static", template_folder="templates")

@analyticsApp.route("/")
def default():
    return render_template('analytics.html')