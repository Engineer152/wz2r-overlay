import os
import requests
import re
import urllib.parse

base_url = "https://api.codmunity.gg/ranked/overlay/"
headers = {
    "x-api-key": os.environ['x-api-key']
}

default = {'skillRating': 0, 'deltaSkillRating': 0, 'rank': 0, 'deltaRank': 0}
# example_data = {"_id":"660ddc2ad88ff6316af162f6","created":1716985263048,"gamertag":"n4noFPS","rank":230,"maxRank":50,"hotstreak":3,"skillRating":14945,"isPro":false,"collec":"warzone-2","season":"year-2024-season-3","maxSkillRating":14945,"bestRank":0,"deltaRank":0,"deltaSkillRating":0,"__v":0,"previousRank":230,"previousSkillRating":14945,"gamertagLc":"n4nofps","id":"660ddc2ad88ff6316af162f6"}

def get_ranked_stats(game,gamertag=""):
    dataout = {'gamertag': gamertag, 'sr': 0, 'dailysr': 0, 'rank': 0, 'dailyrank': 0}
    gamertag=urllib.parse.unquote(gamertag)
    if game=="wz2r":
        game = "warzone-2"
    url = base_url + f"{game}/{gamertag}"
    try: r = requests.get(url,headers=headers,timeout=10)
    except: data = default
    try: data = r.json()
    except: data = default
    if data == None:
        data = default
    if 'skillRating' in data:
        dataout['sr'] = data['skillRating']
        dataout['dailysr'] = data['deltaSkillRating']
        if data['skillRating'] != 0:
            dataout['rank'] = data['rank'] + 1
        dataout['dailyrank'] = data['deltaRank']
    return dataout