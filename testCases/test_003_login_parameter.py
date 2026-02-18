import pytest
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
    @pytest.mark.smoke
    @pytest.mark.parametrize("username,password,expected", test_data)
    def test_login_param(self, setup, username, password, expected):

        driver = setup
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        self.logger.info("====== Login Test Started ======")
        self.logger.info(f"Username: {username} | Expected: {expected}")

        # ---------- LOGIN ACTION ----------
        login_page.enter_username(username)
        login_page.enter_password(password)
        login_page.click_login()

        # ---------- VALID CASE ----------
        if expected == "Valid":

            dashboard_page.wait_for_dashboard_menu()

            assert dashboard_page.is_dashboard_displayed(), \
                "Valid login failed - Dashboard not visible"

            self.logger.info("Valid login successful")

            # Cleanup: Logout for next iteration
            dashboard_page.click_logout()
            login_page.wait_for_login_page()

        # ---------- INVALID CASE ----------
        else:

            assert login_page.is_login_error_displayed(), \
                "Invalid login passed - Error message not shown"

            self.logger.info("Invalid login validation successful")

        self.logger.info("====== Login Test Completed ======")
