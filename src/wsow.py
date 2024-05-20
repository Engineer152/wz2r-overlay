import os
import requests

base_url = "https://api.codmunity.gg/wsow/overlay/"
headers = {
    "x-api-key": os.environ['x-api-key']
}

default = {"teamName":"none","players":[{"name":"Player 1"},{"name":"Player 2"},{"name":"Player 3"}],"rank":0,"points":0,"qualifyingThreshold":0,"lastQualifyingTeamPoints":0}
# default = {"teamName":"none","players":["Player 1","Player 2","Player 3"],"rank":0,"points":0,"topPoints":0,"lastQualifyingTeamPoints":0}

def default_data(teamname):
    default['teamName']=teamname
    return default

def get_wsow_stats(teamname,year,phase,region):
    dataout={}
    if phase == "ingameopen" and region == "na":
        phase = "na-in-game-open"
    url = f"{base_url}{phase}/{teamname}"
    try: r = requests.get(url,headers=headers,timeout=10)
    except: data = default_data(teamname)
    try: data = r.json()
    except: data = default_data(teamname)
    if "teamName" not in data.keys():
        data = default_data(teamname)
    dataout['teamName']=data['teamName'].upper()
    dataout['players']=[data['players'][0]['name'], data['players'][1]['name'], data['players'][2]['name']]
    dataout['rank']=data['rank']
    dataout['points']=data['points']
    dataout['topPlace'] = data['qualifyingThreshold']
    dataout['topPoints'] = data['lastQualifyingTeamPoints']
    return dataout