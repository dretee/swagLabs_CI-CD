from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class loginObjects:
    Username_ID = 'user-name'
    Password_ID = 'password'
    Login_Button_ID = 'login-button'
    Bugger_Button_ID = "react-burger-menu-btn"
    logout_button_ID = 'logout_sidebar_link'

    def __init__(self, driver):
        self.driver = driver

    def GetUserName(self, username):
        element = self.driver.find_element(By.ID, self.Username_ID)
        element.send_keys(username)

    def GetUserPassword(self, Password):
        element = self.driver.find_element(By.ID, self.Password_ID)
        element.send_keys(Password)

    def ClickSubmit(self):
        self.driver.find_element(By.ID, self.Login_Button_ID).click()

    def LogoutSequence(self):
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.ID, self.Bugger_Button_ID))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, self.logout_button_ID))).click()

