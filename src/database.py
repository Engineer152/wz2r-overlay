import pymongo
import os

password=str(os.environ['MONGO_PASS'])
qsbpartner = pymongo.MongoClient(f"mongodb+srv://quickstatsbot:{password}@qsbpartners.o4dvzma.mongodb.net/?retryWrites=true&w=majority")

def add_user(user):
    collection=qsbpartner.WZRanked.Users
    doc = collection.find_one({"season": "season-4" })
    if user not in doc['users']:
        doc['users'] = doc['users'].append()
        collection.replace_one({"season":"season-4"},doc)
    return