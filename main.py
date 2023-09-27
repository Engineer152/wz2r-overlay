from flask import Flask, render_template, request
from src.stats import get_ranked_stats
from src.database import add_user
from turbo_flask import Turbo
import threading
import time
import os
from os.path import exists
import uvicorn
from asgiref.wsgi import WsgiToAsgi
 
app = Flask(__name__)

# Change Version to update All
version = "1.20"

# Standard Colors
bg_color = "F4B228"
name_color = "FFFFFF"
rank_color = "F4B228"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/wz2r/top-250/<language>/<type>/<animated>/<gamertag>", methods=['GET'])
def overlay(language,type,animated,gamertag):
    data = get_ranked_stats(gamertag)
    path_file = f"{language}/{type.upper()}-{animated.upper()}.html"
    if exists("./templates/"+path_file):
        if animated == "acustom" or "scustom":
            try: bg_color = request.args.get('bg_color', default="F4B228")
            except: pass
            bg_color="#"+bg_color
            try: name_color = request.args.get('name_color', default="FFFFFF")
            except: pass
            name_color="#"+name_color
            try: rank_color = request.args.get('rank_color', default=bg_color)
            except: pass
            if rank_color.startswith('#')!=True:
                rank_color="#"+rank_color
            return render_template(path_file, version = version, gamertag = gamertag.capitalize(), sr = data['sr'], dailysr = data['dailysr'], rank = data['rank'], dailyrank = data['dailyrank'],bg_color = bg_color, name_color = name_color, rank_color = rank_color)
        else:
            return render_template(path_file, version = version, gamertag = gamertag.capitalize(), sr = data['sr'], dailysr = data['dailysr'], rank = data['rank'], dailyrank = data['dailyrank'])
    else:
        return render_template("error.html")

@app.route("/backend-data/<gamertag>", methods=['GET'])
def data(gamertag):
    try: add_user(gamertag)
    except: pass
    data = get_ranked_stats(gamertag.lower())
    data['version'] = version
    return data

app = WsgiToAsgi(app)
# ALWAYS CHANGE THIS BACK!!!!!