import pymongo

cluster = pymongo.MongoClient('mongodb://localhost:27017')
# ToDo:: configure regarding your own db in mongo
users = cluster.Bot_Project.test


# add info
def add_user_start(user_id, user_name):
    if not users.find_one({"_id": user_id}):
        users.insert_one({
            "_id": user_id,
            "user_id": str(user_id),
            "user_name": str(user_name),
            "wallet": False
        })
    else:
        pass


def add_user_wallet(user_id, wallet):
    try:
        users.update_one({"_id": user_id}, {"$set": {"wallet": wallet}})
    except:
        pass


# get info
def get_wallet_user(user_id):
    get = users.find_one({"_id": user_id})
    return get['wallet']


def get_user_ids(wallet):
    get = users.find({"wallet": wallet})
    print(get)
    user_ids = [doc["_id"] for doc in get]
    return user_ids
