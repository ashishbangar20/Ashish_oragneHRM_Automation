import pytest
import time
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.buzz_page import BuzzPage
from utilities.config_reader import ReadConfig


@allure.feature("Buzz Module")
@allure.story("Create Buzz Post")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_buzz_post_creation(setup):

    driver = setup
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    buzz_page = BuzzPage(driver)

    allure.dynamic.title("Verify user can create a new Buzz post")

    # ---------- Login ----------
    login_page.login(
        ReadConfig.get_username(),
        ReadConfig.get_password()
    )

    dashboard_page.wait_for_dashboard_menu()

    # ---------- Navigate to Buzz ----------
    buzz_page.click_buzz_menu()

    # ---------- Create Unique Post ----------
    post_message = f"Automation Buzz Post {int(time.time())}"

    buzz_page.post_message(post_message)

    # ---------- Validate Post ----------
    assert buzz_page.is_post_present(post_message), \
        "Buzz post not found after creation"
