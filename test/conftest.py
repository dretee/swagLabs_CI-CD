# General imports
import pytest
from selenium import webdriver

# Imports to get chrome driver working
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Imports to get firefox driver working
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# Import options for headless mode
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Send 'chrome' or 'firefox' as parameter for execution"
    )


@pytest.fixture()
def driver(request):
    browser = request.config.getoption("--browser")

    # Default driver value
    driver = None

    # Chrome and Firefox headless options setup
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')  # Added for stability in headless mode

    firefox_options = FirefoxOptions()
    firefox_options.add_argument('--headless')

    # Setup
    print(f"\nSetting up: {browser} driver")
    if browser == "chrome":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    elif browser == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
    else:
        raise ValueError(f"Browser '{browser}' is not supported. Use 'chrome' or 'firefox'.")

    # Implicit wait setup for the WebDriver
    driver.implicitly_wait(10)

    # Yield driver for use in tests
    yield driver

    # Tear down after tests
    print(f"\nTearing down: {browser} driver")
    driver.quit()
