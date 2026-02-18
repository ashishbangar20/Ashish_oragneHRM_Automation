import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.config_reader import ReadConfig


class TestDashboard:

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_dashboard_loaded(self, setup):

        driver = setup

        login = LoginPage(driver)
        dashboard = DashboardPage(driver)

        # Login
        login.login(
            ReadConfig.get_username(),
            ReadConfig.get_password()
        )

        # Validate dashboard loaded
        dashboard.wait_for_dashboard_menu()

        assert dashboard.is_dashboard_displayed(), \
            "Dashboard not displayed after login"
