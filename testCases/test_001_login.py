import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.config_reader import ReadConfig
from utilities.custom_logger import LogGen


@allure.feature("Login Module")
@allure.story("Valid Login Scenario")
@allure.severity(allure.severity_level.CRITICAL)
class TestLogin:

    logger = LogGen.loggen()

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title("Verify user can login with valid credentials")
    @allure.description("This test verifies that a valid user can successfully login into OrangeHRM.")
    def test_login_valid(self, setup):

        driver = setup
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        username = ReadConfig.get_username()
        password = ReadConfig.get_password()

        self.logger.info("Test Login Started")

        with allure.step("Login using valid credentials"):
            login_page.login(username, password)

        with allure.step("Wait for dashboard to load"):
            dashboard_page.wait_for_dashboard_menu()

        with allure.step("Verify dashboard URL is loaded"):
            assert "dashboard" in driver.current_url.lower()

        self.logger.info("Test Login Completed Successfully")
