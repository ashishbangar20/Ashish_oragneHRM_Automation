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

# ================= CLI OPTIONS ================= #
def pytest_addoption(parser):

    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store", default="false")
    parser.addoption("--env", action="store", default="qa")

@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture()
def headless(request):
    return request.config.getoption("--headless").lower() == "true"

@pytest.fixture()
def environment(request):
    return request.config.getoption("--env")

# ================= DRIVER SETUP ================= #
@pytest.fixture()
def setup(browser, headless):
    driver = None

    # -------- Chrome -------- #
    if browser == "chrome":
        options = ChromeOptions()

        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

    # -------- Firefox -------- #
    elif browser == "firefox":
        options = FirefoxOptions()

        if headless:
            options.add_argument("--headless")

        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)

    # -------- Edge -------- #
    elif browser == "edge":
        options = EdgeOptions()

        if headless:
            options.add_argument("--headless=new")

        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()),options=options)

    else:
        raise ValueError("Browser not supported")

    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver
    driver.quit()

# ================= HTML REPORT ================= #
def pytest_configure(config):

    if not os.path.exists("reports"):
        os.makedirs("reports")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = f"reports/OrangeHRM_Report_{timestamp}.html"

    config.option.htmlpath = report_path
    config.option.self_contained_html = True

    # Metadata
    if hasattr(config, "stash"):
        config.stash[metadata_key]["Project"] = "OrangeHRM Automation"
        config.stash[metadata_key]["Tester"] = "Ashish"
        config.stash[metadata_key]["Framework"] = "Pytest + Selenium"
        config.stash[metadata_key]["Execution"] = "CI/CD"

# ================= SCREENSHOT ON FAILURE ================= #
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):

    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:

        driver = item.funcargs.get("setup")

        if driver:
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)

            file_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)


# ================= OPEN REPORT LOCALLY ================= #
def pytest_sessionfinish(session, exitstatus):

    htmlpath = session.config.option.htmlpath

    # Jenkins / Docker me browser open nahi hona chahiye
    if htmlpath and os.getenv("JENKINS_HOME") is None:

        import webbrowser
        abs_path = os.path.abspath(htmlpath)
        webbrowser.open_new_tab(f"file://{abs_path}")
