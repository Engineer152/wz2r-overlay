import os
import requests

base_url = "https://api.codmunity.gg/wsow/overlay/"
headers = {
    "x-api-key": os.environ['x-api-key']
}

default = {"teamName":"none","players":[{"name":"Player 1"},{"name":"Player 2"},{"name":"Player 3"}],"rank":0,"points":0,"kills":0,'topPlace':0,'topPoints':0,'topPoints':0,}
# default = {"teamName":"none","players":["Player 1","Player 2","Player 3"],"rank":0,"points":0,"qualifyingThreshold":'-',"lastQualifyingTeamPoints":'-'}

def default_data(teamname):
    default['teamName']=teamname
    return default

def get_wsow_stats(region,teamname):
    dataout={'topPlace':0,'topPoints':0,'topPointsDiff':0,"kills":0}
    if region.lower() == "eu":
        region = "emea"
    elif region.lower() == "global":
        region = "all"
    url = base_url + f"{region}/{teamname}"
    try: r = requests.get(url,headers=headers,timeout=10)
    except: data = default_data(teamname)
    try: data = r.json()
    except: data = default_data(teamname)
    if "teamName" not in data.keys():
        data = default_data(teamname)
    dataout['teamName']=data['teamName'].upper()
    players = []
    for p in data['players']:
        try: players.append(p['name'][0:7])
        except: players.append("-")
    if len(players) < 3:
        players.extend(['-','-','-'])
    dataout['players']=players
    dataout['rank']=data['rank']
    try: dataout['kills']=data['kills']
    except: dataout['kills']=0
    dataout['points']=data['points']
    dataout['topPointsDiff']=data['points'] - data['topPoints']
    if 'qualifyingThreshold' in data:
        dataout['topPlace'] = f"TOP{data['qualifyingThreshold']}"
        dataout['topPoints'] = data['lastQualifyingTeamPoints']
    return dataout