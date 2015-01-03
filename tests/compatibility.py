from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import common
import unittest
import time

# Expects the browser to render the homepage correctly
class LatestBrowserTest(unittest.TestCase):

    def __init__(self, browser, version=None):
        caps = browser
        if version is not None:
            caps['version'] = version

        # Change the report name to something more readable, see https://spoon.net/reports
        caps['name'] = "X-Browser Compatibility"

        # spoon.net hub image defaults to port 4444
        self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", desired_capabilities=caps)
        
        self.testbrowsers()
        self.tearDown()

    def testbrowsers(self):
        self.driver.get("https://spoon.net");
        print("Looking for homepage element")
        homeContent = self.driver.find_element_by_id("home-content")
        self.assertTrue(homeContent.is_displayed())
        print("Success!")

    def tearDown(self):
        self.driver.quit()
        
# Expects the browser to redirect to the unsupported page
class FailBrowserTest(unittest.TestCase):

    def __init__(self, browser, version):        
        caps = browser
        caps['version'] = version
        caps['name'] = "X-Browser Compatibility"
        self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", desired_capabilities=caps)
        self.testbrowsers()
        self.tearDown()

    def testbrowsers(self):
        self.driver.get("https://spoon.net");
        print("Homepage element should not exist and should be redirected to unsupported page")

        try:
            self.driver.find_element_by_id("home-content")
            self.assertTrue(False, "home-content should not exist")
        except NoSuchElementException:
            self.assertTrue(True)
        
        print("Make sure page has unsupported image")
        unsupported = self.driver.find_element_by_xpath("//img[@src='/images/logo_unsupported.png']")
        self.assertTrue(unsupported.is_displayed())
        print("Success!")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # Test latest supported browsers
    print("Testing latest Chrome")
    suite.addTest(LatestBrowserTest(webdriver.DesiredCapabilities.CHROME))
    print("Testing latest Firefox")
    suite.addTest(LatestBrowserTest(webdriver.DesiredCapabilities.FIREFOX))
    # Test an unsupported browser
    print("Testing Internet Explorer 6")
    print("Please be patient this one takes awhile to start!")
    suite.addTest(FailBrowserTest(webdriver.DesiredCapabilities.INTERNETEXPLORER, "6"))

    runner = unittest.TextTestRunner()
