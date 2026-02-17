import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


class TestLogout:

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_logout(self, setup):

        driver = setup
        login = LoginPage(driver)
        dashboard = DashboardPage(driver)

        login.enter_username("Admin")
        login.enter_password("admin123")
        login.click_login()


        dashboard.wait_for_dashboard_menu()
        dashboard.click_logout()

        assert "login" in driver.current_url.lower()
