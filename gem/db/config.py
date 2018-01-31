from pymongo import MongoClient
import configparser
config = configparser.ConfigParser()
config.read("config.ini")

host = config.get("db", "host", fallback="127.0.0.1")
port = config.getint("db", "port", fallback="27017")
name = config.get("db", "name", fallback="gem")

client = MongoClient(host, port)
database = client[name]

proposals = database["proposals"]
users = database["users"]
sessions = database["sessions"]
votes = database["votes"]
comments = database["comments"]
roles = database["roles"]
laws = database["laws"]
articles = database["articles"]
orders = database["orders"]
services = database["services"]
