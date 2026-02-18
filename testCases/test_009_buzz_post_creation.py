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
        self.logger.info("====== Buzz Post Test Started ======")

        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        buzz_page = BuzzPage(driver)

        # Login
        login_page.login(
            ReadConfig.get_username(),
            ReadConfig.get_password()
        )

        dashboard_page.wait_for_dashboard_menu()

        # Navigate to Buzz
        buzz_page.click_buzz_menu()

        # Unique message
        post_message = f"Automation Buzz Post {int(time.time())}"

        buzz_page.post_message(post_message)

        # Validate post created
        assert buzz_page.is_post_present(post_message), \
            "Buzz post not found after creation"

        self.logger.info("====== Buzz Post Test Passed ======")
