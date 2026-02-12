import time
import webbrowser
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from utilities.config_reader import ReadConfig
import os
from datetime import datetime
from pytest_metadata.plugin import metadata_key


# Browser Selection Option

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")

@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")

# Setup Fixture

@pytest.fixture()
def setup(browser):

    if browser == "chrome":
        driver = webdriver.Chrome(service=ChromeService())

    elif browser == "edge":
        driver = webdriver.Edge(service=EdgeService())

    elif browser == "firefox":
        driver = webdriver.Firefox(service=FirefoxService())

    else:
        raise ValueError("Browser not supported")

    driver.get(ReadConfig.get_url())
    driver.maximize_window()

    yield driver
    driver.quit()

# Dynamic HTML Report Path
def pytest_configure(config):

    if not os.path.exists("reports"):
        os.makedirs("reports")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = f"reports/OrangeHRM_Report_{timestamp}.html"

    config.option.htmlpath = report_path
    config.option.self_contained_html = True


    if hasattr(config, "stash"):
        config.stash[metadata_key]["Project"] = "OrangeHRM Automation"
        config.stash[metadata_key]["Tester"] = "Ashish"
        config.stash[metadata_key]["Environment"] = "QA"

def pytest_sessionfinish(session, exitstatus):
    htmlpath = session.config.option.htmlpath

    if htmlpath:
        abs_path = os.path.abspath(htmlpath)

        # ⭐ Important wait (report file generate hone ke liye)
        time.sleep(2)

        webbrowser.open_new_tab(f"file://{abs_path}")
