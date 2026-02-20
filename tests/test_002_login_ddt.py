import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.login_xl_reader import LoginDataReader
from utilities.data_paths import TEST_DATA_PATH


@allure.feature("Login Module")
@allure.story("DDT Login using Excel Data")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize(
    "username,password,expected",
    LoginDataReader.get_login_data(TEST_DATA_PATH, "sheet_one")
)
def test_login_ddt(setup, username, password, expected):

    driver = setup
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    # Dynamic test title in Allure
    allure.dynamic.title(f"Login Test | User: {username} | Expected: {expected}")

    with allure.step(f"Enter Username: {username}"):
        login_page.enter_username(username)

    with allure.step("Enter Password"):
        login_page.enter_password(password)

    with allure.step("Click Login Button"):
        login_page.click_login()

    is_dashboard = "dashboard" in driver.current_url.lower()

    if expected == "Valid":

        with allure.step("Validate successful login"):
            assert is_dashboard, "Expected login to succeed but it failed"

        with allure.step("Logout after successful login"):
            dashboard_page.click_logout()
            login_page.wait_for_login_page()

    else:

        with allure.step("Validate login failure"):
            assert not is_dashboard, "Expected login to fail but it succeeded"
