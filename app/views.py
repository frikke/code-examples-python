"""Defines the home page route"""

from flask import render_template, url_for, redirect, Blueprint, current_app as app
from .ds_config import DS_CONFIG

from .ds_config import EXAMPLES_API_TYPE

core = Blueprint("core", __name__)


@core.route("/")
def index():
    if EXAMPLES_API_TYPE["Rooms"]:
        return render_template(
            "home_rooms.html", title="Home - Python Rooms API Code Examples"
        )
    if DS_CONFIG["quickstart"] == "true":
        return redirect(url_for("core.qshome"))
    else:
        return render_template("home.html", title="Home - Python Code Examples")

@core.route("/quickstarthome")
def qshome():
    return render_template("quickstarthome.html", title = "Homepage for Quickstart")

@core.route("/index")
def r_index():
    return redirect(url_for("core.index"))

@core.app_errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@core.app_errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500
