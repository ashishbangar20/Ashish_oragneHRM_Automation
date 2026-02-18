import pytest
import allure
from pages.login_page import LoginPage


@allure.feature("Login Module")
@allure.story("Empty Credential Validation")
@pytest.mark.regression
@pytest.mark.smoke
def test_empty_login(setup):

    driver = setup
    login = LoginPage(driver)

    allure.dynamic.title("Verify required validation message on empty login")

    # Click login without entering credentials
    login.click_login()

    # Validate required field error
    assert login.is_required_error_displayed(), \
        "Required error message not displayed"
