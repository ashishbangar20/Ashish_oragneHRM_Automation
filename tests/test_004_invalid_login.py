import pytest
import allure
from pages.login_page import LoginPage


@allure.feature("Login Module")
@allure.story("Invalid Login Validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
@pytest.mark.smoke
def test_invalid_login(setup):

    driver = setup
    login = LoginPage(driver)

    allure.dynamic.title("Verify Invalid Login Shows Error Message")
    allure.dynamic.description(
        "Ensure that login fails with incorrect credentials "
        "and appropriate error message is displayed."
    )

    with allure.step("Enter invalid username"):
        login.enter_username("Admin")

    with allure.step("Enter invalid password"):
        login.enter_password("wrongpass")

    with allure.step("Click Login button"):
        login.click_login()

    with allure.step("Verify error message is displayed"):
        assert login.is_login_error_displayed(), \
            "Error message not displayed for invalid login"
