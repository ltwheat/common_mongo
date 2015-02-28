#!/usr/bin/env

import pymongo

# Was gonna make this an object/class, but I don't think it makes that much
# sense for a non-persistent class
#class BaseDao(object):
#    def __init__(self):
client = pymongo.MongoClient()

### Mongodb notes ###
#   1) Connection/Client -> Database -> Collection
#      b) client=pymongo.MongoClient()
#         db=pymongo.database.Database(client, "db_name")
#         db.coll_name.insert({"sample":"dict"})
#      b) client=pymongo.MongoClient()
#         db=client['db_name']
#         coll=db['coll_name']
#         coll.insert({"sample":"dict"})
#   2) Collection won't actually exist until data is inserted
#   3) Commonly used gets:
#      a) coll/conn.database_names()# returns all db names
#      b) db.collection_names()# returns all collection names in db
#      c) coll.find_one()# returns (random?) single item from coll
#      d) list(coll.find())# returns everything in coll. Must be cast

def get_db(db_name):
    try:
        return client[db_name]
    except pymongo.errors.ConnectionFailure:
        print("Could not connect to database")

def get_coll(db_name, coll_name):
    db = get_db(db_name)
    return db[coll_name]

def store_object(db_name, coll_name, obj):
    coll = get_coll(db_name, coll_name)
    return coll.insert(obj)

def get_all_coll_objects(db_name, coll_name):
    coll = get_coll(db_name, coll_name)
    return coll.find()
