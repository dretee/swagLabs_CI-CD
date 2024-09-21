import pytest
from selenium.webdriver.common.by import By
from Utilities.Logger import Information_Logger
from src.LoginObjects import loginObjects


class TestLoginDDT001:
    base_url = "https://www.saucedemo.com"
    logger = Information_Logger.logging_info()

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
        # Initialize loginObjects
        self.li = loginObjects(self.driver)
        self.li.GetUserName("standard_user")
        self.li.GetUserPassword("secret_sauce")
        self.li.ClickSubmit()
        assert "Swag Labs" in self.driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
            "***** TEST FAILED ******")
        self.logger.info("***** TEST PASSED ******")

    # Negative Tes Cases
    @pytest.mark.parametrize("username, password, error_message", [
        ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
        ("invalidUser", "invalidPass", "Epic sadface: Username and password do not match any user in this service"),
        ('', '', 'Epic sadface: Username is required')])
    def test_invalid_user_login(self, driver, username, password, error_message):
        self.driver = driver
        self.page_navigation(self.driver)
        self.logger.info("***** TESTING INVALID LOGIN ******")
        self.li = loginObjects(driver)
        self.li.GetUserName(username)
        self.li.GetUserPassword(password)
        self.li.ClickSubmit()
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert error_message in body_text, self.logger.info("***** TEST FAILED ******")
        self.logger.info("***** TEST PASSED ******")
