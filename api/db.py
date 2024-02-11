from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import json

uri = "mongodb+srv://kura:Elnino123456789@cluster0.afwuy4j.mongodb.net/?retryWrites=true&w=majority"

client  = None
database = None
collection = None

# Create a new client and connect to the server
with open("config.json","r+") as f:
    config_json = json.load(f)
    client = MongoClient(config_json['URI'], server_api=ServerApi('1'))

    database = client["Gtech"]
    collection = database["Gtech"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def retrieve_users(s_id):
    return collection.find_one({"seqn":int(s_id)},{ "seqn": 1, "age": 1, "first": 1 })

