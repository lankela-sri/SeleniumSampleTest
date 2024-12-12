import pytest
from selenium import webdriver
import configparser

@pytest.fixture(scope='session')
def config():
    config = configparser.ConfigParser()
    config.read('tests/config.ini')
    return config

@pytest.fixture(params=[(1024, 768), (768, 1024), (375, 667), (414, 896)])
def viewport_size(request):
    return request.param

@pytest.fixture(scope="session")
def driver(config):
    if config['DEFAULT']['Browser'] == "Firefox":
        return webdriver.Firefox()
    elif config['DEFAULT']['Browser'] == "Chrome":
        return webdriver.Chrome()

def test_responsive_layout(driver, config, viewport_size):
    driver.set_window_size(*viewport_size)
    driver.get(config['DEFAULT']['BaseUrl'])
    assert driver.get_window_size()['width'] == viewport_size[0], "Width should match"
    assert driver.get_window_size()['height'] == viewport_size[1], "Height should match"