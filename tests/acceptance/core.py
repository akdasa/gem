import unittest

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
