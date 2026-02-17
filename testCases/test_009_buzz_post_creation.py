import pytest
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.buzz_page import BuzzPage
from utilities.config_reader import ReadConfig
from utilities.custom_logger import LogGen


class TestBuzz:

    logger = LogGen.loggen()

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_buzz_post_creation(self, setup):

        driver = setup
        self.logger.info("Test Buzz Post Creation Started")

        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        buzz_page = BuzzPage(driver)

        username = ReadConfig.get_username()
        password = ReadConfig.get_password()

        # Login
        login_page.enter_username(username)
        login_page.enter_password(password)
        login_page.click_login()
        dashboard_page.wait_for_dashboard_menu()

        # Navigate to Buzz
        buzz_page.click_buzz_menu()

        # Unique post message
        post_message = f"Automation Buzz Post {int(time.time())}"

        buzz_page.enter_post_message(post_message)
        buzz_page.click_post_button()

        self.logger.info("Buzz Post Button Clicked Successfully")
