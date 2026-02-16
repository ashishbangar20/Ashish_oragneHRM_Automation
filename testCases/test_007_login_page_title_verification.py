import pytest


class TestLoginPageUI:

    @pytest.mark.regression
    @pytest.mark.sanity
    def test_login_page_title(self, setup):

        driver = setup

        assert "OrangeHRM" in driver.title
