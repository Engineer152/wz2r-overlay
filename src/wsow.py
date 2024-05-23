import os
import requests
from src.database import wsow_current

base_url = "https://api.codmunity.gg/wsow/overlay/"
headers = {
    "x-api-key": os.environ['x-api-key']
}

default = {"teamName":"none","players":[{"name":"Player 1"},{"name":"Player 2"},{"name":"Player 3"}],"rank":0,"points":0,"topPlace":'-',"topPoints":'-'}
# default = {"teamName":"none","players":["Player 1","Player 2","Player 3"],"rank":0,"points":0,"qualifyingThreshold":'-',"lastQualifyingTeamPoints":'-'}

def default_data(teamname):
    default['teamName']=teamname
    return default

def get_wsow_stats(region,teamname):
    dataout={'topPlace':'-','topPoints':'-'}
    url = base_url + f"{region}/{teamname}"
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
    if data['qualifyingThreshold']:
        dataout['topPlace'] = f"TOP{data['qualifyingThreshold']}"
        dataout['topPoints'] = data['lastQualifyingTeamPoints']
    return dataout