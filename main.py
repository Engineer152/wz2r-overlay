from flask import Flask, render_template, request, redirect
from src.stats import get_ranked_stats
from src.camo import get_camo_stats, get_new_camo_stats
from src.wsow import get_wsow_stats, get_wsow_player_stats
from turbo_flask import Turbo
import threading
import time
import os
from os.path import exists
import uvicorn
from asgiref.wsgi import WsgiToAsgi
 
app = Flask(__name__)

# Change Version to update All
version = "1.57"

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
@app.route("/<game>/top-250/<language>/<type>/<animated>/<gamertag>", methods=['GET'])
def overlay(game,language,type,animated,gamertag):
    data = get_ranked_stats(game,gamertag.lower())
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
            return render_template(path_file, version = version, gamertag = gamertag.capitalize(), game = game, sr = data['sr'], dailysr = data['dailysr'], rank = data['rank'], dailyrank = data['dailyrank'],bg_color = bg_color, name_color = name_color, rank_color = rank_color)
        else:
            return render_template(path_file, version = version, gamertag = gamertag.capitalize(), game = game, sr = data['sr'], dailysr = data['dailysr'], rank = data['rank'], dailyrank = data['dailyrank'])
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
    
# NEW Camos camo/{typeofcamo}/{username}
@app.route("/camo-new/<typeofcamo>/<username>", methods=['GET'])
def camo_new(typeofcamo,username):
    data = get_new_camo_stats(typeofcamo,username)
    path_file = f"camo/english/CAMO-NEW-STATIC-SM.html"
    if exists("./templates/"+path_file):
        return render_template(path_file, version = version, data = data, typeofcamo=typeofcamo, username=username)
    else:
        return render_template("error.html")

@app.route("/wsow/<region>/<teamname>", methods=['GET'])
def wsow(region: str,teamname: str):
    path_file = f"wsow/english/HORIZONTAL-STATIC-2025.html"
    # try: text = request.args.get('text', default="")
    # except: text = ""
    data = get_wsow_stats(region,teamname)
    if exists("./templates/"+path_file):
        return render_template(path_file, version=version, backgroundImage=data['backgroundImage'], teamname=str(data['teamName'].strip()), isteam=data['IsTeam'], players=data['players'], rank=data['rank'], points=data['points'], kills=data['kills'], topPlace=data['topPlace'], topPoints=data['topPoints'], topPointsDiff=data['topPointsDiff'], region=region, textnote=text)
    else:
        return render_template("error.html")
    
@app.route("/wsow/<player>", methods=['GET'])
def wsow_player(player: str):
    path_file = f"wsow/english/HORIZONTAL-STATIC-2025-PLAYER.html"
    data = get_wsow_player_stats(player)
    if exists("./templates/"+path_file):
        return render_template(path_file, version=version, backgroundImage=data['backgroundImage'], teamname=str(data['teamName'].strip()), isteam=data['IsTeam'], players=data['players'], rank=data['rank'], points=data['points'], kills=data['kills'], topPlace=data['topPlace'], topPoints=data['topPoints'], topPointsDiff=data['topPointsDiff'], region="", textnote=text)
    else:
        return render_template("error.html")
    
@app.route("/test/wsow/<region>/<teamname>", methods=['GET'])
def wsow_test(region: str,teamname: str):
    path_file = f"wsow/english/HORIZONTAL-STATIC-2025.html"
    try: text = request.args.get('text', default="")
    except: pass
    data = get_wsow_stats(region,teamname)
    if exists("./templates/"+path_file):
        return render_template(path_file, version=version, backgroundImage=data['backgroundImage'], teamname=str(data['teamName'].strip()), isteam=data['IsTeam'], players=data['players'], rank=data['rank'], points=data['points'], kills=data['kills'], topPlace=data['topPlace'], topPoints=data['topPoints'], topPointsDiff=data['topPointsDiff'], region=region, textnote=text)
    else:
        return render_template("error.html")

@app.route("/backend-data/<game>/<gamertag>", methods=['GET'])
def ranked_data(game,gamertag):
    data = get_ranked_stats(game,gamertag.lower())
    data['version'] = version
    return data

#TEMP FIX REMOVE AFTER 7/30/2024
@app.route("/backend-data/<gamertag>", methods=['GET'])
def old_data(gamertag):
    data = get_ranked_stats("wz2r",gamertag.lower())
    data['version'] = version
    return data
# <----------------------------------->

@app.route("/update-camo/<typeofcamo>/<username>", methods=['GET'])
def camo_data(typeofcamo,username):
    data = get_camo_stats(typeofcamo,username)
    data['version'] = version
    return data

@app.route("/update-camo-new/<typeofcamo>/<username>", methods=['GET'])
def camo_new_data(typeofcamo,username):
    data = get_new_camo_stats(typeofcamo,username)
    data['version'] = version
    return data

@app.route("/update-wsow-team/<region>/<teamname>", methods=['GET'])
def wsow_data(region: str,teamname: str):
    data = get_wsow_stats(region,teamname)
    data['version'] = version
    return data

@app.route("/update-wsow-player/<player>", methods=['GET'])
def wsow_player_data(player: str):
    data = get_wsow_player_stats(player)
    data['version'] = version
    return data

app = WsgiToAsgi(app)

# ALWAYS CHANGE THIS BACK!!!!!
