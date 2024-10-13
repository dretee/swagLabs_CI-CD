import requests
from selenium.webdriver.common.by import By
from Utilities.Logger import Information_Logger
from Utilities import generalInfor


class Test_linkVerification:
    # Initialize class variables
    base_url = generalInfor.base_url
    logger = Information_Logger.logging_info()
    Username_ID = generalInfor.Username_ID
    Password_ID = generalInfor.Password_ID
    Login_Button_ID = generalInfor.Login_Button_ID

    def test_linkchecker_01(self, driver):
        # Initialize driver and navigate to the application URL
        self.logger.info("******* TEST TO CHECK LINKS FUNCTIONALITY (test_linkchecker_01) ***********")
        self.logger.info("******* INITIALIZING THE DRIVER AND OPENING THE WEBPAGE ***********")
        self.driver = driver
        self.driver.get(self.base_url)
        self.driver.maximize_window()

        # Login to the application
        self.logger.info("******* LOGIN SEQUENCE INITIATED, GETTING THE USERNAME AND THE PASSWORD ***********")

        element = self.driver.find_element(By.ID, self.Username_ID)
        element.send_keys("standard_user")

        element1 = self.driver.find_element(By.ID, self.Password_ID)
        element1.send_keys("secret_sauce")
        self.driver.find_element(By.ID, self.Login_Button_ID).click()
        # Get all links on the page
        all_links = self.driver.find_elements(By.TAG_NAME, "a")
        self.logger.info(f"The total number of links on this page is {len(all_links)}")

        # Initialize counters for broken and functional links
        count_broken = 0

        # Iterate through all links and check their status
        for link in all_links:
            url = link.get_attribute("href")
            try:
                response = requests.head(url)
            except:
                response = None

            if response is not None and response.status_code >= 400:
                count_broken += 1
                self.logger.info(f"THIS LINK {link} IS BROKEN")
            else:
                self.logger.info(f"THIS LINK {link} IS FUNCTIONAL")

        # Log the total number of broken and functional links
        self.logger.info(f"TOTAL BROKEN LINKS: {count_broken}")
        self.logger.info(f"TOTAL FUNCTIONAL LINKS: {len(all_links) - count_broken}")

        # Assert that there are no broken links
        assert count_broken == 0, "TEST FAILED: THERE ARE BROKEN LINKS ON THE PAGE"
        self.logger.info("TEST PASSED: ALL LINKS ARE FUNCTIONAL")
