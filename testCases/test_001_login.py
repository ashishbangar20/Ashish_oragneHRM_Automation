import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.config_reader import ReadConfig
from utilities.custom_logger import LogGen


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

        login_page.login(username, password)
        dashboard_page.wait_for_dashboard_menu()

        assert "dashboard" in driver.current_url.lower()

        self.logger.info("Test Login Completed Successfully")
