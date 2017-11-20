from tests.acceptance.core import Test


class ProposalsTestCase(Test):
    def test_add_proposal(self):
        self.__add_proposal("New proposal 123", "Some content")
        self.driver.get("http://127.0.0.1:5000/proposals/")
        assert self.__check_proposal_in_table("New proposal 123") is not None

    def __add_proposal(self, title, content):
        self.driver.get("http://127.0.0.1:5000/proposals/")
        self.driver.find_element_by_id("proposals-new").click()
        self.driver.find_element_by_name("title").send_keys(title)
        self.driver.find_element_by_name("content").send_keys(content)
        self.driver.find_element_by_id("submit").click()

    def __check_proposal_in_table(self, title):
        return self.driver.find_element_by_xpath("//a[text() = '{}']".format(title))