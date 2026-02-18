import os
import pytest
import allure
import subprocess
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from pytest_metadata.plugin import metadata_key
from utilities.config_reader import ReadConfig


# ================= CLI OPTIONS ================= #

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store", default="false")


@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser").lower()


@pytest.fixture()
def headless(request):
    return request.config.getoption("--headless").lower() == "true"


# ================= DRIVER SETUP ================= #

@pytest.fixture()
def setup(browser, headless):

    driver = None
    grid_url = os.getenv("GRID_URL")

    print("\n========== Execution Info ==========")
    print(f"Browser   : {browser}")
    print(f"Headless  : {headless}")
    print(f"GRID_URL  : {grid_url}")
    print("====================================\n")

    if browser == "chrome":
        options = ChromeOptions()

        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        if os.path.exists("/usr/bin/chromium"):
            options.binary_location = "/usr/bin/chromium"

        if grid_url:
            driver = webdriver.Remote(command_executor=grid_url, options=options)
        else:
            driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")

        if grid_url:
            driver = webdriver.Remote(command_executor=grid_url, options=options)
        else:
            driver = webdriver.Firefox(options=options)

    elif browser == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless=new")

        if grid_url:
            driver = webdriver.Remote(command_executor=grid_url, options=options)
        else:
            driver = webdriver.Edge(options=options)

    else:
        raise ValueError(f"Browser not supported: {browser}")

    driver.implicitly_wait(5)
    driver.get(ReadConfig.get_url())

    yield driver

    driver.quit()


# ================= REPORT CONFIG ================= #

def pytest_configure(config):

    # ✅ Force Allure results directory (important)
    if not config.option.allure_report_dir:
        config.option.allure_report_dir = "allure-results"

    os.makedirs("allure-results", exist_ok=True)

    # ---------- HTML REPORT (UNCHANGED) ----------
    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = f"reports/report_{timestamp}.html"

    config.option.htmlpath = report_path
    config.option.self_contained_html = True

    if hasattr(config, "stash"):
        config.stash[metadata_key]["Project"] = "OrangeHRM Automation"
        config.stash[metadata_key]["Tester"] = "Ashish"
        config.stash[metadata_key]["Execution"] = "CI/CD"
        config.stash[metadata_key]["Environment"] = "Docker/Grid/Local"


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
            file_path = os.path.join("screenshots", file_name)

            driver.save_screenshot(file_path)
            print(f"Screenshot saved: {file_path}")

            # ✅ Attach screenshot to Allure
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )


# ================= SESSION FINISH ================= #

def pytest_sessionfinish(session, exitstatus):

    # 🚫 Do NOT open Allure in Jenkins/Docker
    if os.getenv("JENKINS_HOME") or os.getenv("GRID_URL"):
        return

    # Open HTML locally
    htmlpath = session.config.option.htmlpath
    if htmlpath:
        import webbrowser
        webbrowser.open_new_tab(f"file://{os.path.abspath(htmlpath)}")

    # Open Allure locally
    if os.path.exists("allure-results"):
        subprocess.run(
            ["allure", "generate", "allure-results", "-o", "allure-report", "--clean"]
        )
        subprocess.run(["allure", "open", "allure-report"])
