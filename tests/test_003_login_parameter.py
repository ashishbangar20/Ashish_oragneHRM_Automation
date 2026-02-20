import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@allure.feature("Login Module")
@allure.story("Parametrized Login Validation")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("Admin", "admin123", "Valid"),
        ("Admin", "wrongpass", "Invalid"),
        ("WrongUser", "admin123", "Invalid"),
        ("WrongUser", "wrongpass", "Invalid"),
    ]
)
def test_login_param(setup, username, password, expected):

    driver = setup
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    # Dynamic title in Allure
    allure.dynamic.title(
        f"Login Test | User: {username} | Expected: {expected}"
    )

    with allure.step(f"Enter Username: {username}"):
        login_page.enter_username(username)

    with allure.step("Enter Password"):
        login_page.enter_password(password)

    with allure.step("Click Login Button"):
        login_page.click_login()

    # ================= VALID CASE =================
    if expected == "Valid":

        with allure.step("Wait for Dashboard to Load"):
            dashboard_page.wait_for_dashboard_menu()

        with allure.step("Verify Dashboard is Displayed"):
            assert dashboard_page.is_dashboard_displayed(), \
                "Valid login failed - Dashboard not visible"

        with allure.step("Logout to reset session"):
            dashboard_page.click_logout()
            login_page.wait_for_login_page()

    # ================= INVALID CASE =================
    else:

        with allure.step("Verify Login Error Message Displayed"):
            assert login_page.is_login_error_displayed(), \
                "Invalid login passed - Error message not shown"
