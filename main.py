from flask import Flask, render_template
from src.stats import get_ranked_stats
from turbo_flask import Turbo
import threading
import time
import os
from os.path import exists
import uvicorn
from asgiref.wsgi import WsgiToAsgi
 
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/wz2r/top-250/<language>/<type>/<animated>/<gamertag>", methods=['GET'])
def overlay(language,type,animated,*,gamertag):
    data = get_ranked_stats(gamertag)
    path_file = f"{language}/{type.upper()}-{animated.upper()}.html"
    if exists("./templates/"+path_file):
        return render_template(path_file, gamertag = gamertag.capitalize(), sr = data['sr'], dailysr = data['dailysr'], rank = data['rank'], dailyrank = data['dailyrank'])
    else:
        return render_template("error.html")

@app.route("/backend-data/<gamertag>", methods=['GET'])
def data(gamertag):
    data = get_ranked_stats(gamertag.lower())
    return data

app = WsgiToAsgi(app)