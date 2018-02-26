#Example 0:@ 2017-03-09 13:22
#For normal WebDriver scripts (non-Remote), the Java server is not needed.
#However, to use Selenium Webdriver Remote or the legacy Selenium API (Selenium-RC), 
#you need to also run the Selenium server. The server requires a Java Runtime Environment (JRE).

#Download the server separately, from: http://selenium-release.storage.googleapis.com/3.3/selenium-server-standalone-3.3.0.jar

#Run the server from the command line:
#java -jar selenium-server-standalone-3.3.0.jar
#Then run your Python client scripts.
#Use The Source Luke!
#open a new Firefox browser
#load the page at the given URL
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://seleniumhq.org/')
Example 1:

open a new Firefox browser
load the Yahoo homepage
search for “seleniumhq”
close the browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get('http://www.yahoo.com')
assert 'Yahoo!' in browser.title

elem = browser.find_element_by_name('p')  # Find the search box
elem.send_keys('seleniumhq' + Keys.RETURN)

browser.quit()
Example 2:

Selenium WebDriver is often used as a basis for testing web applications. Here is a simple example uisng Python’s standard unittest library:

import unittest

class GoogleTestCase(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.addCleanup(self.browser.quit)

    def testPageTitle(self):
        self.browser.get('http://www.google.com')
        self.assertIn('Google', self.browser.title)

if __name__ == '__main__':
    unittest.main(verbosity=2)
Selenium Server (optional)



