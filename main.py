from flask import Flask, render_template, request, redirect
from src.stats import get_ranked_stats
from src.camo import get_camo_stats
from src.wsow import get_wsow_stats
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
version = "1.43"

# Standard Colors
bg_color = "F4B228"
name_color = "FFFFFF"
rank_color = "F4B228"
text = ""

@app.route("/")
def index():
    return redirect('https://codmunity.gg/overlay')
    # return render_template("index.html")

#WZ2 Ranked
@app.route("/wz2r/top-250/<language>/<type>/<animated>/<gamertag>", methods=['GET'])
def overlay(language,type,animated,gamertag):
    data = get_ranked_stats(gamertag)
    path_file = f"ranked/{language}/{type.upper()}-{animated.upper()}.html"
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

# WZ3 Camos camo/{typeofcamo}/{username}
@app.route("/camo/<typeofcamo>/<username>", methods=['GET'])
def camo(typeofcamo,username):
    data = get_camo_stats(typeofcamo,username)
    path_file = f"camo/english/CAMO-STATIC.html"
    if exists("./templates/"+path_file):
        return render_template(path_file, version = version, data = data, bg_color = bg_color, name_color = name_color, rank_color = rank_color)
    else:
        return render_template("error.html")

# WSOW Teams wsow/<year>/<type>/<reigon>/<teamname>
@app.route("/wsow/<region>/<teamname>", methods=['GET'])
def wsow(region: str,teamname: str):
    path_file = f"wsow/english/HORIZONTAL-STATIC-NO-TEAM.html"
    try: text = request.args.get('text', default="")
    except: text = ""
    data = get_wsow_stats(region,teamname)
    if exists("./templates/"+path_file):
        if text != "":
            return render_template(f"wsow/english/HORIZONTAL-STATIC-TEXT.html", version=version, teamname=str(data['teamName'].strip()), players=data['players'], rank=data['rank'], points=data['points'], topPlace=data['topPlace'], topPoints=data['topPoints'], region=region, textnote=text)
        else:
            return render_template(path_file, version=version, teamname=str(data['teamName'].strip()), players=data['players'], rank=data['rank'], points=data['points'], topPlace=data['topPlace'], topPoints=data['topPoints'], region=region, textnote=text)
    else:
        return render_template("error.html")
    
@app.route("/test/wsow/<region>/<teamname>", methods=['GET'])
def wsow_test(region: str,teamname: str):
    path_file = f"wsow/english/HORIZONTAL-STATIC.html"
    try: text = request.args.get('text', default="")
    except: pass
    data = get_wsow_stats(region,teamname)
    if exists("./templates/"+path_file):
        return render_template(path_file, version=version, teamname=str(data['teamName'].strip()), players=data['players'], rank=data['rank'], points=data['points'], topPlace=data['topPlace'], topPoints=data['topPoints'], region=region, textnote=text)
    else:
        return render_template("error.html")

@app.route("/backend-data/<gamertag>", methods=['GET'])
def data(gamertag):
    try: add_user(gamertag)
    except: pass
    data = get_ranked_stats(gamertag.lower())
    data['version'] = version
    return data

@app.route("/update-camo/<typeofcamo>/<username>", methods=['GET'])
def camo_data(typeofcamo,username):
    data = get_camo_stats(typeofcamo,username)
    data['version'] = version
    return data

@app.route("/update-wsow-team/<region>/<teamname>", methods=['GET'])
def wsow_data(region: str,teamname: str):
    data = get_wsow_stats(region,teamname)
    data['version'] = version
    return data

app = WsgiToAsgi(app)
# ALWAYS CHANGE THIS BACK!!!!!