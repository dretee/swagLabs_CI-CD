from selenium.webdriver.common.by import By

from PageObjects.AddtocartObejects import AddcartObject
from Utilities.Logger import Information_Logger
from Utilities import generalInfor


class TestCheckOutProcess:
    # Initialize class variables
    base_url = generalInfor.base_url
    logger = Information_Logger.logging_info()
    Username_ID = generalInfor.Username_ID
    Password_ID = generalInfor.Password_ID
    Login_Button_ID = generalInfor.Login_Button_ID

    def test_checkoutPayment_01(self, driver):
        # This payment method encompasses the selection and ordering of items,
        # followed by providing accurate payment information during the checkout process.

        # Initialize driver and navigate to the application URL
        self.logger.info("******* TEST TO CHECKOUT (test_checkout) ***********")
        self.logger.info("******* INITIALIZING THE DRIVER AND OPENING THE WEBPAGE***********")
        self.driver = driver
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        # Login to the application
        self.logger.info("******* LOGIN SEQUENCE INITIATED, GETTING THE USERNAME AND THE PASSWORD***********")
        element = self.driver.find_element(By.ID, self.Username_ID)
        element.send_keys("standard_user")

        element1 = self.driver.find_element(By.ID, self.Password_ID)
        element1.send_keys("secret_sauce")
        self.driver.find_element(By.ID, self.Login_Button_ID).click()

        # Add items to the cart
        self.logger.info("******* ADDING ITEMS TO CART ***********")
        self.ac = AddcartObject(self.driver)
        list_of_items = [self.ac.addFleece_Jacket, self.ac.addT_Shirt_Red, self.ac.addOnesie,
                         self.ac.addBackpack, self.ac.addBike_Light, self.ac.addBolt_TShirt]
        for index in range(0, len(list_of_items), 2):
            items = list_of_items[index]
            items()  # Calling the functions to add items to the cart

        # Navigate to the cart and calculate total prices
        self.logger.info("******* NAVIGATING TO CART AND CALCULATING TOTAL PRICES ***********")
        self.ac.Cart_click()
        total = 0
        cart_item_prices = self.driver.find_elements(By.XPATH, "//div[@class='inventory_item_price']")
        for price in cart_item_prices:
            prices = (float(price.text.replace("$", "")))
            total += prices
        print(f"the total price of all the goods is {total}")

        # Proceed to checkout and compare total prices
        self.logger.info("******* PROCEEDING TO CHECKOUT ***********")
        self.ac.Checkout_button()
        self.ac.inputTxtLastname("Anthony")
        self.ac.inputTxtFirstname("Uyah")
        self.ac.inputTxtZipcode("9985101")
        self.ac.CheckoutContinue()

        total_price_element = self.driver.find_element(By.XPATH, "//div[@class='summary_subtotal_label']")
        total_price = (float(total_price_element.text.replace("Item total: $", "")))
        if total_price == total:
            # If total prices match, complete the order
            self.ac.Finishbutton_click()
            self.ac.LogoutSequence()
            actual_text = self.driver.find_element(By.XPATH,
                                                   "//h2[normalize-space()='Thank you for your order!']").text

            displayed_text = "Thank you for your order!"
            assert actual_text.__eq__(displayed_text), "*********** TEST FAILED ************"
            self.logger.info("******** TEST WAS SUCCESSFUL *********")

    def test_checkoutpayment_02(self, driver):
        # This payment method encompasses the selection and ordering of NO items,
        # followed by providing inaccurate payment information during the checkout process.

        # Initialize driver and navigate to the application URL
        self.logger.info("******* TEST TO CHECKOUT WITHOUT ORDERING ITEMS (test_checkoutpayment_02) ***********")
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

        # Proceed to checkout without ordering items
        self.logger.info("******* PROCEEDING TO CHECKOUT WITHOUT ORDERING ITEMS ***********")
        self.ac = AddcartObject(self.driver)
        self.ac.Cart_click()
        self.ac.Checkout_button()

        # Provide inaccurate payment information
        self.logger.info("******* PROVIDING INACCURATE PAYMENT INFORMATION ***********")
        self.ac.inputTxtLastname("Anthony")
        self.ac.inputTxtFirstname("Uyah")
        # Inputting wrong code in the zipcode input box
        self.ac.inputTxtZipcode("bl875ef")
        self.ac.CheckoutContinue()
        self.ac.Finishbutton_click()

        # Verify if the order was not placed successfully
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        displayed_text = "Thank you for your order!"  # Displayed message when an order has been placed
        assert displayed_text not in body_text, "******* TEST FAILED: ORDER WAS PLACED WITH NO ITEM ORDERED *******"
        self.logger.info("******* TEST SUCCESSFUL: THE ORDER WAS NOT PLACED ********")
