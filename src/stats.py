import pymongo
import requests
import re
import urllib.parse
from src.database import curr_season

client=pymongo.MongoClient("mongodb://userranked:UserRanked@15.235.43.233/test?authMechanism=DEFAULT",27017)
db = client.test.rankedplayers

def live_data(gamertag=""):
    url = "https://telescope.callofduty.com/api/ts-api/lb/v1/global/title/wz2/ranked/br"
    r = requests.get(url)
    resp = r.json()
    players = resp['data']['data']['ranks']
    for p in players:
        if p['gamertag'].lower() == gamertag.lower():
            return p['skillRating'], p['rank']+1
    return None

def get_ranked_stats(gamertag=""):
    # season = curr_season()
    # gamertag=urllib.parse.unquote(gamertag)
    data = {'sr': 0, 'dailysr': 0, 'rank': 0, 'dailyrank': 0}
    # coll = db.find({'gamertag': re.compile(gamertag, re.IGNORECASE), 'season': season})
    # coll = list(coll)
    # for x in coll:
    #     if x['gamertag'].lower() == gamertag.lower():
    #         coll = x
    # # coll = db.find_one({'gamertag': re.compile(gamertag, re.IGNORECASE), 'season': 'season-5'})
    # if type(coll) == dict:
    #     data['sr'] = coll['skillRating']
    #     data['dailysr'] = coll['deltaSkillRating']
    #     data['rank'] = coll['rank'] + 1
    #     data['dailyrank'] = coll['deltaRank']
    # else:
    #     try: data['sr'], data['rank'] = live_data(gamertag)
    #     except: pass
    return data