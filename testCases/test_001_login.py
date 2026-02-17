import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.config_reader import ReadConfig
from utilities.custom_logger import LogGen
from utilities.screenshot import capture_screenshot


class TestLogin:

    logger = LogGen.loggen()

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_valid(self, setup):

        driver = setup

        self.logger.info("Test Login Started")

        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        username = ReadConfig.get_username()
        password = ReadConfig.get_password()

        login_page.enter_username(username)
        login_page.enter_password(password)
        login_page.click_login()
        dashboard_page.wait_for_dashboard_menu()

        if "dashboard" in driver.current_url.lower():
            self.logger.info("Login Test Passed")
            assert True
        else:
            self.logger.error("Login Test Failed")
            capture_screenshot(driver, "test_login_valid")
            assert False
