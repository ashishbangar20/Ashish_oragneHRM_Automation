import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.config_reader import ReadConfig


@allure.feature("Dashboard Module")
@allure.story("Dashboard Load Verification")
@pytest.mark.smoke
@pytest.mark.regression
def test_dashboard_loaded(setup):

    driver = setup
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)

    allure.dynamic.title("Verify dashboard loads after successful login")

    # Login
    login.login(
        ReadConfig.get_username(),
        ReadConfig.get_password()
    )

    # Wait for dashboard
    dashboard.wait_for_dashboard_menu()

    # Validation
    assert dashboard.is_dashboard_displayed(), \
        "Dashboard did not load after login"
