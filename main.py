from flask import Flask, render_template
from src.stats import get_ranked_stats
from turbo_flask import Turbo
import threading
import time
import os
import uvicorn
from asgiref.wsgi import WsgiToAsgi
 
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/wz2r/top-250/<language>/<type>/<animated>/<gamertag>", methods=['GET'])
def overlay(language,type,animated,gamertag):

    data = get_ranked_stats(gamertag)

    return render_template(f"{language}/{type}-{animated}.html", gamertag = gamertag.capitalize(), sr = data['sr'], dailysr = data['dailysr'], rank = data['rank'], dailyrank = data['dailyrank'])

@app.route("/backend-data/<gamertag>", methods=['GET'])
def data(gamertag):
    data = get_ranked_stats(gamertag.lower())
    return data

app = WsgiToAsgi(app)