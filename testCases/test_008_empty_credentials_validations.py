import pytest
from pages.login_page import LoginPage


class TestEmptyLogin:

    @pytest.mark.regression
    @pytest.mark.smoke
    def test_empty_login(self, setup):

        driver = setup
        login = LoginPage(driver)

        login.click_login()

        assert login.is_required_error_displayed(), \
            "Required error message not displayed"
