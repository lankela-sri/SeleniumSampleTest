import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
import os

# Configuration setup fixture
@pytest.fixture(scope='session')
def get_config():
    config = configparser.ConfigParser()
    config_path = os.path.join('tests', 'config.ini')  # Ensure the path is correct relative to where pytest is run.
    config.read(config_path)
    return config

# WebDriver setup fixture
@pytest.fixture(scope="session")
def driver(get_config):
    config = get_config
    browser_name = config['DEFAULT']['Browser']  # Correctly retrieving the browser name from config file.

    if browser_name == "Firefox":
        driver = webdriver.Firefox()
    elif browser_name == "Chrome":
        driver = webdriver.Chrome()
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    login_url = config['LOGIN']['OrangeHrmUrl']
    driver.get(login_url)
    yield driver
    driver.quit()

def test_navigate_and_refresh(driver):
    # WebDriver wait
    wait = WebDriverWait(driver, 10)

    # Clicking on a specific element using WebDriverWait
    forgot_password_link = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//p[@class='oxd-text oxd-text--p orangehrm-login-forgot-header']"))
    )
    forgot_password_link.click()

