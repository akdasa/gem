from pymongo import MongoClient


def prepare_database():
    client = MongoClient('192.168.56.100', 27017)
    client.drop_database("gbcma")
    client["gbcma"]["users"].insert({
        "login": "test",
        "password": "test",
        "name": "Tester das",
        "permissions": [
            "proposals.create", "proposals.read", "proposals.update", "proposals.delete",
            "users.create", "users.read", "users.update", "users.delete"
        ]
    })
