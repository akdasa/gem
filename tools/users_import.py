# PYTHONPATH=. python3.6 ./tools/users_import.py
import csv

from gem.db import users



def _is_user_exist(name):
    user = users.find_one({"name": name})
    return user is not None

with open("./tools/passwords.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        if not _is_user_exist(row[0]):
            users.insert({
                "name": row[0],
                "login": row[0],
                "role": row[1],
                "password": row[2]
            })
            print(row[0], "created")
        else:
            user = users.find_one({"name": row[0]})
            user.name = row[0]
            user.login = row[0]
            user.role = row[1]
            user.password = row[2]
            users.save(user)
            print(user.name, "updated")
