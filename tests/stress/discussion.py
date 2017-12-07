import random
from threading import Thread
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

session_id = "5a13ff0686d5a01839d47c1e"
host = "http://127.0.0.1:5000"

chrome_options = Options()
chrome_options.add_argument("--headless")


def run(login, password):
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("{}/account/login".format(host))
    sleep(1)

    driver.find_element_by_name("login").send_keys(login)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_id("signin").click()

    driver.get("{}/session/{}".format(host, session_id))
    sleep(1)

    for i in range(1, 10):
        random_button = random.choice(["raise-hand", "withdraw-hand"])
        driver.find_element_by_id("discussion-{}".format(random_button)).click()
        sleep(3)

    sleep(15)
    print("Close user {}".format(login))
    driver.close()


for i in range(1, 25):
    user_id = "user{}".format(i)
    print("Start user {}".format(i))
    thread = Thread(target=run, args=(user_id, user_id))
    thread.start()
    sleep(1)
