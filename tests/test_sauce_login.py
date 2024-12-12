import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import configparser
import os
import time

# Configuration Setup
@pytest.fixture(scope='session')
def get_config():
    """Fixture to load and return config data from a file."""
    config = configparser.ConfigParser()
    # Be sure of the path relative to where pytest is run; adjust if needed
    config_path = os.path.join('tests', 'config.ini')
    config.read(config_path)
    return config

# Driver Setup
@pytest.fixture(scope="session")
def driver(get_config):
    """Fixture to initialize and teardown the Selenium WebDriver."""
    config = get_config
    browser_name = config['DEFAULT']['Browser']
    if browser_name == "Firefox":
        driver = webdriver.Firefox()
    elif browser_name == "Chrome":
        driver = webdriver.Chrome()
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    login_url = config['LOGIN']['LoginUrl']
    driver.get(login_url)
    yield driver
    driver.quit()

### Test Definitions

def test_login(driver, get_config):
    """Tests the login functionality based on configured credentials."""
    config = get_config
    username_field = driver.find_element(By.ID, config['LOCATORS']['UsernameField'])
    password_field = driver.find_element(By.ID, config['LOCATORS']['PasswordField'])
    login_button = driver.find_element(By.ID, config['LOCATORS']['LoginButton'])

    username_field.send_keys(config['LOGIN']['Username'])
    password_field.send_keys(config['LOGIN']['Password'])
    login_button.click()

    # Verification
    # Wait for elements to be visible, implies explicit wait or use of WebDriverWait
    # For simplicity, time.sleep is used. Recommended: WebDriverWait with conditions
    time.sleep(2)  # Pause to wait for navigation or UI update; not recommended for real tests
    success_element = driver.find_element(By.CSS_SELECTOR, ".title")
    assert success_element.text == "Products", f"Expected page title after login should be 'Products' not '{success_element.text}'"