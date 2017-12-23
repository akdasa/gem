import random
from gem.db import users

roles = ["Deputy", "GBC", "Guest", "Minister"]

for i in range(1, 100):
    user_id = "user{}".format(i)
    random_role = random.choice(roles)
    users.insert({
        "name": user_id,
        "login": user_id,
        "password": user_id,
        "role": random_role
    })
