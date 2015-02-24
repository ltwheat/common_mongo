#!/usr/bin/env

import base_conn

# In terms of scaling, the smasher/fighter/stage division will be per database,
# since, for instance, smash and League info shouldn't be on the same db
# anyway. But for now, the local database will be them all and we'll divide
# everything by collections
#smash_db_name = "smash_wii_u"
smash_db_name = "test_db"
fgm_coll_name = "for_glory_matches"
smasher_coll_name = "smashers"
# Constants are probably good enough for these, at least for now, since there
# are a set number (there won't be enough DLC to justify otherwise) and it's
# just a name-to-id relationship, but just naming the dbs for consistency
fighter_coll_name = "fighters"
stage_coll_name = "stages"

def get_all_matches():
    return base_conn.get_all_coll_objects(smash_db_name, smasher_coll_name)

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
        db_match_id = coll.insert(match)
        print("Stored match of id {0}:".format(match_id))
        return db_match_id
    except pymongo.errors.DuplicateKeyError as dke:
        print(dke)

# TODO: Fill out args, return values
def get_smasher():
    pass

def get_all_smashers():
    coll = base_conn.get_coll(smash_db_name, smasher_coll_name)
    return coll.find()

def store_smasher(smasher):
    smashers = get_all_smashers()
    return base_conn.store_object(smash_db_name, smasher_coll_name, smasher)
