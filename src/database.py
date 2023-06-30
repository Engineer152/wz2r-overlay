import pymongo
import os

password=str(os.environ['MONGO_PASS'])
qsbpartner = pymongo.MongoClient(f"mongodb+srv://quickstatsbot:{password}@qsbpartners.o4dvzma.mongodb.net/?retryWrites=true&w=majority")

def add_user(user):
    collection=qsbpartner.WZRanked.Users
    doc = collection.find_one({"season": "season-4" })
    current = doc['users']
    if user not in current:
        current.append(str(user))
        doc['users'] = current
        collection.replace_one({"season":"season-4"},doc)
    return