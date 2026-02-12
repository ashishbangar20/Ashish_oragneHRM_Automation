import pytest
from pages.login_page import LoginPage
from utilities.custom_logger import LogGen


@pytest.mark.regression
class TestInvalidLogin:

    logger = LogGen.loggen()

    def test_invalid_login(self, setup):

        self.logger.info("Invalid Login Test Started")

        driver = setup
        login = LoginPage(driver)

        login.enter_username("Admin")
        login.enter_password("wrongpass")
        login.click_login()

        assert "dashboard" not in driver.current_url.lower()
