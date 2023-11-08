import pymongo
import json
from pymongo import MongoClient, InsertOne

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["Topology_Manager"]
collection = db["Tree_Topologies"]

requesting = [1,2,3,4,5]

mydict = { "name": "John", "address": "Highway 378" }

x = collection.insert_one(mydict)


