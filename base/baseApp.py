from flask import Blueprint, render_template, redirect,url_for

baseApp = Blueprint("baseApplication", __name__, static_folder="static", template_folder="templates")

@baseApp.route("/")
def default():
    return redirect(url_for('lineApplication.default'))
