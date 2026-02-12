import pytest
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.custom_logger import LogGen


class TestLoginParametrized:

    logger = LogGen.loggen()

    test_data = [
        ("Admin", "admin123", "Valid"),
        ("Admin", "wrongpass", "Invalid"),
        ("WrongUser", "admin123", "Invalid"),
        ("WrongUser", "wrongpass", "Invalid")
    ]

    @pytest.mark.regression
    @pytest.mark.parametrize("username,password,expected", test_data)
    def test_login_param(self, setup, username, password, expected):

        self.logger.info("====== Starting Parametrized Login Test ======")
        self.logger.info(f"Username: {username}")
        self.logger.info(f"Expected: {expected}")

        driver = setup

        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        login_page.enter_username(username)
        login_page.enter_password(password)
        login_page.click_login()

        time.sleep(2)

        is_dashboard = "dashboard" in driver.current_url.lower()

        # ✅ VALID CASE
        if expected == "Valid":

            if is_dashboard:
                self.logger.info("Login Passed")
                dashboard_page.click_logout()
                assert True
            else:
                self.logger.error("Login Failed")
                assert False

        # ❌ INVALID CASE
        elif expected == "Invalid":

            if not is_dashboard:
                self.logger.info("Invalid Login Correct")
                assert True
            else:
                self.logger.error("Invalid Login Passed")
                dashboard_page.click_logout()
                assert False
