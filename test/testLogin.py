import pytest
from selenium.webdriver.common.by import By
from Utilities.Logger import Information_Logger
from Utilities import generalInfor


class TestLoginDDT001:
    base_url = generalInfor.base_url
    logger = Information_Logger.logging_info()
    Username_ID = generalInfor.Username_ID
    Password_ID = generalInfor.Password_ID
    Login_Button_ID = generalInfor.Login_Button_ID

    def page_navigation(self, driver):
        # Initialize the test and log the start
        self.logger.info("***** STARTING THE TEST ******")
        self.logger.info("***** STARTING THE LOGIN HOMEPAGE TEST ******")

        # Set up the WebDriver and navigate to the base URL
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        self.logger.info("***** NAVIGATING TO THE TEST PAGE ******")

    def test_homepage_navigation(self, driver):
        self.driver = driver
        # Url navigation
        self.page_navigation(self.driver)
        # Get the actual title of the page
        actual_title = self.driver.title
        assert actual_title == "Swag Labs", self.logger.info("***** TEST FAILED ******")
        self.logger.info("***** TEST PASSED ******")

    def test_login_for_correct_details(self, driver):
        self.driver = driver
        # Url navigation
        self.page_navigation(self.driver)
        self.logger.info("***** NAVIGATING TO THE TEST PAGE ******")
        element = self.driver.find_element(By.ID, self.Username_ID)
        element.send_keys("standard_user")

        element1 = self.driver.find_element(By.ID, self.Password_ID)
        element1.send_keys("secret_sauce")
        self.driver.find_element(By.ID, self.Login_Button_ID).click()
        assert "Swag Labs" in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
            "***** THIS TEST FAILED ******")
        self.logger.info("***** THIS TEST PASSED ******")

    # Negative Test Cases Data and Test Script
    test_data = [
        ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
        ("invalidUser", "invalidPass", "Epic sadface: Username and password do not match any user in this service"),
        ('', '', 'Epic sadface: Username is required')
    ]

    @pytest.mark.parametrize("username, password, error_message", test_data)
    def test_invalid_user_login(self, driver, username, password, error_message):
        self.driver = driver
        self.page_navigation(self.driver)
        self.logger.info("***** TESTING INVALID LOGIN ******")

        element = self.driver.find_element(By.ID, self.Username_ID)
        element.send_keys(username)

        element1 = self.driver.find_element(By.ID, self.Password_ID)
        element1.send_keys(password)
        self.driver.find_element(By.ID, self.Login_Button_ID).click()
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert error_message in body_text, self.logger.info("***** TEST FAILED ******")
        self.logger.info("***** TEST PASSED ******")
