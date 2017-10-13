from pymongo import MongoClient

client = MongoClient('192.168.56.100', 27017)
database = client["gbcma"]

proposals = database["proposals"]
users = database["users"]
sessions = database["sessions"]
