import pytest
from selenium import webdriver
from sys import platform
from config import BASE_URL, BASE_DIR
from config import LOGGING_CONFIG
import logging
import logging.config
import os
import sys
from yaml import load


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser type: chrome, firefox.")
    parser.addoption("--logger", action="store", default="DEBUG", help="Logger level: INFO, DEBUG, WARNING ERROR.")
    parser.addoption("--headless", action="store_true", default=False, help="To run chrome in headless mode.")


@pytest.fixture()
def driver(request):

    global BROWSER

    BROWSER = pytest.config.getoption("--browser")
    headless = pytest.config.getoption("--headless")

    print("Browser: {}".format(BROWSER))

    if BROWSER == 'chrome':
        chrome_options = _get_chrome_options(False)
        if headless:
            print("Run test in headless mode: --headless")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")

        if platform in ('darwin', 'linux', 'linux2'):
            d = webdriver.Chrome(chrome_options=chrome_options)
        else:  # win64
            chrome_path = os.path.join(BASE_DIR, 'drivers', 'win', 'chromedriver.exe')
            d = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)
    else:
        print("unrecognized browser: {}".format(BROWSER))
        sys.exit(1)

    d.get(BASE_URL)
    d.maximize_window()
    yield d
    #  teardown
    d.quit()


@pytest.fixture()
def logger():

    LEVEL = pytest.config.getoption("--logger")
    print("Logger: {}".format(LEVEL))
    logging.config.dictConfig(LOGGING_CONFIG)
    log = logging.getLogger('main')
    log.setLevel(level=logging.getLevelName(LEVEL))
    return log


@pytest.fixture()
def yaml():
    with open(os.path.join(BASE_DIR, "config.yaml"), 'r') as yaml_file:
        return load(yaml_file)


def _get_chrome_options(caps=False):

    opts = webdriver.ChromeOptions()
    prefs = dict()
    prefs["credentials_enable_service"] = False
    prefs["password_manager_enabled"] = False
    opts.add_experimental_option("prefs", prefs)
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-infobars")
    if caps:
        return opts.to_capabilities()
    else:
        return opts

