import unittest

from bson import ObjectId
from pymongo import MongoClient

from selenium import webdriver


class Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.authenticate("secretary", "pwd")

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def authenticate(self, login, password):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/account/login")
        driver.find_element_by_id("login").clear()
        driver.find_element_by_id("login").send_keys(login)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("signin").click()
        assert driver.current_url is not "http://127.0.0.1:5000/account"

    def clean_database(self):
        client = MongoClient('192.168.56.100', 27017)
        client.drop_database("gbcma")

        client["gbcma"]["roles"].insert({
            "name" : "Depute",
            "permissions" : [
                "proposals.read",
                "session.join",
                "vote"
            ]
        })

        client["gbcma"]["roles"].insert({
            "name": "GBC",
            "permissions": [
                "proposals.read",
                "session.join",
                "vote"
            ]
        })

        client["gbcma"]["roles"].insert({
            "name" : "Secretary",
            "permissions" : [
                "proposals.create",
                "proposals.read",
                "proposals.update",
                "proposals.delete",
                "users.create",
                "users.read",
                "users.update",
                "users.delete",
                "sessions.create",
                "sessions.read",
                "sessions.update",
                "sessions.delete",
                "session.manage",
                "roles.create",
                "roles.read",
                "roles.update",
                "roles.delete"
            ]
        })

