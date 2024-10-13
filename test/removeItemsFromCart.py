
from selenium.webdriver.common.by import By

from Utilities.Logger import Information_Logger
from Utilities import generalInfor
from PageObjects.AddtocartObejects import AddcartObject


class TestAddRemoveToCart:
    base_url = generalInfor.base_url
    logger = Information_Logger.logging_info()
    Username_ID = generalInfor.Username_ID
    Password_ID = generalInfor.Password_ID
    Login_Button_ID = generalInfor.Login_Button_ID

    def test_removeFromCart(self, driver):

        # Initialize driver and navigate to the application URL
        self.logger.info("******* TEST TO REMOVE ITEMS FROM THE CART (test_remove from cart) ***********")
        self.logger.info("******* INITIALIZING THE DRIVER AND OPENING THE WEBPAGE***********")
        self.driver = driver
        self.driver.get(self.base_url)
        self.driver.maximize_window()

        # Login sequence
        self.logger.info("******* LOGIN SEQUENCE INITIATED, GETTING THE USERNAME AND THE PASSWORD***********")

        element = self.driver.find_element(By.ID, self.Username_ID)
        element.send_keys("standard_user")

        element1 = self.driver.find_element(By.ID, self.Password_ID)
        element1.send_keys("secret_sauce")
        self.driver.find_element(By.ID, self.Login_Button_ID).click()

        # Adding items to the cart
        self.ac = AddcartObject(self.driver)
        items_to_add = [self.ac.addFleece_Jacket, self.ac.addT_Shirt_Red, self.ac.addOnesie,
                        self.ac.addBackpack, self.ac.addBike_Light, self.ac.addBolt_TShirt]
        counts = 0

        for index in range(0, len(items_to_add), 2):
            item_function = items_to_add[index]
            item_function()  # Call the function at the even index
            counts += 1
            self.logger.info(F"******* ADDITION OF THE ITEM {counts}***********")

        self.ac.Cart_click()  # go to cart

        # Remove all items from the cart
        item_to_remove = [self.ac.removeFleece_Jacket, self.ac.removeT_Shirt_Red, self.ac.removeOnesie,
                          self.ac.removeBackpack, self.ac.removeBike_Light, self.ac.removeBolt_TShirt]
        count = 0
        for items in range(0, len(item_to_remove), 2):
            item_removal = item_to_remove[items]
            item_removal()  # Call the function at the even item
            count += 1
            self.logger.info(F"******* REMOVAL OF THE ITEM {count}***********")
        body_text = self.driver.find_element(By.TAG_NAME, "body").text

        # Proceed to check the item removed via the number displayed on the cart icon
        item_list = ["Sauce Labs Fleece Jacket",
                     "Test.allTheThings() T-Shirt (Red)",
                     "Sauce Labs Onesie",
                     "Sauce Labs Backpack",
                     "Sauce Labs Bike Light",
                     "Sauce Labs Bolt T-Shirt"]
        if all(items not in body_text for items in item_list):
            self.logger.info("Items were removed from the cart successfully.")
            assert True
        else:
            self.logger.error("Items were not removed from the cart correctly.")
            assert False
