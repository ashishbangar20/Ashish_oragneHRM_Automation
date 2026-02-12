import pytest


@pytest.mark.sanity
class TestLoginPageUI:

    def test_login_page_title(self, setup):

        driver = setup

        assert "OrangeHRM" in driver.title
