import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.config_reader import ReadConfig


class TestLogout:

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_logout(self, setup):

        driver = setup
        login = LoginPage(driver)
        dashboard = DashboardPage(driver)

        # Login
        login.enter_username(ReadConfig.get_username())
        login.enter_password(ReadConfig.get_password())
        login.click_login()

        dashboard.wait_for_dashboard_menu()

        # Logout
        dashboard.click_logout()

        # Wait for login page
        login.wait_for_login_page()

        # Validate login page visible
        assert login.is_login_page_displayed(), "Logout failed - Login page not visible"
