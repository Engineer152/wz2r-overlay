import pymongo
import os

password=str(os.environ['MONGO_PASS'])
qsbpartner = pymongo.MongoClient(f"mongodb+srv://quickstatsbot:{password}@qsbpartners.o4dvzma.mongodb.net/?retryWrites=true&w=majority")

def curr_season():
    collection=qsbpartner.WZRanked.General
    doc = collection.find_one({})
    s = doc['current']
    return s

def add_user(user):
    collection=qsbpartner.WZRanked.Users
    season = curr_season()
    doc = collection.find_one({"season": season})
    if doc == None:
        doc = {"season": season, "users": []}
        collection.insert_one(doc)
    current = doc['users']
    if user not in current:
        current.append(str(user))
        doc['users'] = current
        collection.replace_one({"season": season},doc)
    return