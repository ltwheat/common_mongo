#!/usr/bin/env

# TODO: This is a band-aid, ultimately should only need to import pymongo in
#       base_conn (needed for DuplicateKeyError)
import pymongo

# Not sure why "import base_conn" doesn't work
from common_mongo import base_conn

# In terms of scaling, the smasher/fighter/stage division will be per database,
# since, for instance, smash and League info shouldn't be on the same db
# anyway. But for now, the local database will be them all and we'll divide
# everything by collections

smash_db_name = "smash_wii_u"
#smash_db_name = "test_db"
fgm_coll_name = "for_glory_matches"
smasher_coll_name = "smashers"
# Constants are probably good enough for these, at least for now, since there
# are a set number (there won't be enough DLC to justify otherwise) and it's
# just a name-to-id relationship, but just naming the dbs for consistency
fighter_coll_name = "fighters"
stage_coll_name = "stages"

def get_smash_db():
    return base_conn.get_db(smash_db_name)

def get_all_matches():
    return list(base_conn.get_all_coll_objects(smash_db_name, fgm_coll_name))

def store_match(match):
    matches = get_all_matches()
    # TODO: This check loops through every match in the db but I feel like
    #       that probably won't scale? Should we keep a separate coll of
    #       just match ids?
    match_id = matches.count() 
    match['match_id'] = match_id
    try:
        for db_match in matches:
            if match_id == db_match['match_id']:
                err_msg = "Match with id {0} already found in " \
                           "collection".format(match_id)
                raise pymongo.errors.DuplicateKeyError(err_msg)
        db_match_id = base_conn.store_object(smash_db_name, fgm_coll_name,
                                             match)
        print("\nStored match of id {0}:".format(db_match_id))
        return db_match_id
    except pymongo.errors.DuplicateKeyError as dke:
        print(dke)

def get_smasher_coll():
    smash_db = get_smash_db()
    return smash_db[smasher_coll_name]

def get_smasher(smasher_dict):
    return get_smasher_coll().find_one(smasher_dict)

def get_all_smashers():
    smashers = base_conn.get_all_coll_objects(smash_db_name, smasher_coll_name)
    return list(smashers)

def store_smasher(smasher):
    smasher_dict = smasher.convert_to_dict()
    if smasher.tag == '':
        raise AttributeError("Can't store Smasher with no tag")
    elif smasher.smasher_id < 0:
        raise AttributeError("Can't store Smasher with no id")
    return base_conn.store_object(smash_db_name, smasher_coll_name,
                                  smasher_dict)
