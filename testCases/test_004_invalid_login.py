import pytest
from pages.login_page import LoginPage
from utilities.custom_logger import LogGen


class TestInvalidLogin:

    logger = LogGen.loggen()

    @pytest.mark.regression
    @pytest.mark.smoke
    def test_invalid_login(self, setup):

        driver = setup
        login = LoginPage(driver)

        self.logger.info("====== Invalid Login Test Started ======")

        login.enter_username("Admin")
        login.enter_password("wrongpass")
        login.click_login()

        # Validate error message instead of URL
        error_displayed = login.is_login_error_displayed()

        assert error_displayed, "Error message not displayed for invalid login"

        self.logger.info("====== Invalid Login Test Passed ======")
