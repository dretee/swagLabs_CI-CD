import pytest
from selenium.webdriver.common.by import By
from Utilities.Logger import Information_Logger


class TestLoginDDT001:
    base_url = "https://www.saucedemo.com"
    logger = Information_Logger.logging_info()
    Username_ID = 'user-name'
    Password_ID = 'password'
    Login_Button_ID = 'login-button'

    def page_navigation(self, driver):
        # Initialize the test and log the start
        self.logger.info("***** STARTING THE TEST ******")
        self.logger.info("***** STARTING THE LOGIN HOMEPAGE TEST ******")

        # Set up the WebDriver and navigate to the base URL
        driver.get(self.base_url)
        driver.maximize_window()
        self.logger.info("***** NAVIGATING TO THE TEST PAGE ******")

    def test_homepage_navigation(self, driver):

        # Url navigation
        self.page_navigation(driver)
        # Get the actual title of the page
        actual_title = driver.title
        assert actual_title == "Swag Labs", self.logger.info("***** TEST FAILED ******")
        self.logger.info("***** TEST PASSED ******")

    def test_login_for_correct_details(self, driver):
        # Url navigation
        self.page_navigation(self.driver)
        self.logger.info("***** NAVIGATING TO THE TEST PAGE ******")
        element = driver.find_element(By.ID, self.Username_ID)
        element.send_keys("standard_user")

        element1 = driver.find_element(By.ID, self.Password_ID)
        element1.send_keys("secret_sauce")
        self.driver.find_element(By.ID, self.Login_Button_ID).click()
        assert "Swag Labs" in driver.find_element(By.TAG_NAME, "body").text, self.logger.info(
            "***** THIS TEST FAILED ******")
        self.logger.info("***** THIS TEST PASSED ******")

    # Negative Tes Cases
    @pytest.mark.parametrize("username, password, error_message", [
        ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
        ("invalidUser", "invalidPass", "Epic sadface: Username and password do not match any user in this service"),
        ('', '', 'Epic sadface: Username is required')])
    def test_invalid_user_login(self, driver, username, password, error_message):

        self.page_navigation(self.driver)
        self.logger.info("***** TESTING INVALID LOGIN ******")

        element = driver.find_element(By.ID, self.Username_ID)
        element.send_keys(username)

        element1 = driver.find_element(By.ID, self.Password_ID)
        element1.send_keys(password)
        driver.find_element(By.ID, self.Login_Button_ID).click()
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert error_message in body_text, self.logger.info("***** TEST FAILED ******")
        self.logger.info("***** TEST PASSED ******")
