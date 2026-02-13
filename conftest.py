import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from pytest_metadata.plugin import metadata_key
from utilities.config_reader import ReadConfig

# ================= CLI OPTIONS ================= #

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store", default="false")


@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture()
def headless(request):
    return request.config.getoption("--headless").lower() == "true"


# ================= DRIVER SETUP ================= #

@pytest.fixture()
def setup(browser, headless):

    browser = browser.lower()
    driver = None

    # -------- CHROME -------- #
    if browser == "chrome":

        options = ChromeOptions()

        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--remote-allow-origins=*")

        driver_path = ChromeDriverManager().install()

        # Mac webdriver fix
        if "THIRD_PARTY" in driver_path:
            driver_path = driver_path.replace(
                "THIRD_PARTY_NOTICES.chromedriver",
                "chromedriver"
            )

        driver = webdriver.Chrome(
            service=ChromeService(driver_path),
            options=options
        )

    # -------- FIREFOX -------- #
    elif browser == "firefox":

        options = FirefoxOptions()

        if headless:
            options.add_argument("--headless")

        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )

    # -------- EDGE -------- #
    elif browser == "edge":

        options = EdgeOptions()

        if headless:
            options.add_argument("--headless=new")

        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )

    else:
        raise ValueError(f"Browser not supported: {browser}")

    driver.set_page_load_timeout(30)
    driver.get(ReadConfig.get_url())

    yield driver
    driver.quit()


# ================= HTML REPORT ================= #

def pytest_configure(config):

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config.option.htmlpath = f"reports/report_{timestamp}.html"
    config.option.self_contained_html = True

    if hasattr(config, "stash"):
        config.stash[metadata_key]["Project"] = "OrangeHRM Automation"
        config.stash[metadata_key]["Tester"] = "Ashish"
        config.stash[metadata_key]["Execution"] = "CI/CD"


# ================= SCREENSHOT ON FAILURE ================= #

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):

    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:

        driver = item.funcargs.get("setup")

        if driver:
            os.makedirs("screenshots", exist_ok=True)

            file_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(os.path.join("screenshots", file_name))


# ================= OPEN REPORT LOCALLY ================= #

def pytest_sessionfinish(session, exitstatus):

    htmlpath = session.config.option.htmlpath

    if htmlpath and os.getenv("JENKINS_HOME") is None:

        import webbrowser
        webbrowser.open_new_tab(f"file://{os.path.abspath(htmlpath)}")
