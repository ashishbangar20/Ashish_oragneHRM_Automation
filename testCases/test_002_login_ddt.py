import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.login_xl_reader import LoginDataReader
from utilities.data_paths import TEST_DATA_PATH


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

    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()

    is_dashboard = "dashboard" in driver.current_url.lower()

    if expected == "Valid":
        assert is_dashboard
        dashboard_page.click_logout()
        login_page.wait_for_login_page()
    else:
        assert not is_dashboard
