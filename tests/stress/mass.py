from random import choice
from threading import Thread
from time import sleep

from socketIO_client import SocketIO, LoggingNamespace

stage = None

def user_thread(login, password):
    s = SocketIO('localhost', 5000, LoggingNamespace)

    s.emit("login", {"login": login, "password": password})
    s.emit("join", {'room': roomId})

    while True:
        if stage == "vote":
            s.emit("vote", {"value": choice(["yes", "no", "undecided"])})

        #s.emit("chat", {"msg": "Hello{}".format(stage)})
        sleep(1)


for i in range(1, 10):
    roomId = "5a13ff0686d5a01839d47c1e"
    userId = "user{}".format(i)
    thread = Thread(target=user_thread, args=(userId, userId))
    thread.start()

while True:
    stage = input("stage> ")