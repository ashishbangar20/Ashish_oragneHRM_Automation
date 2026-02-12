import pytest
from pages.login_page import LoginPage


@pytest.mark.regression
class TestEmptyLogin:

    def test_empty_login(self, setup):

        driver = setup
        login = LoginPage(driver)

        login.click_login()

        assert "Required" in driver.page_source
