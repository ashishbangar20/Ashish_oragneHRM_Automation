from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):

    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    LOGIN_ERROR = (By.XPATH, "//p[contains(@class,'oxd-alert-content-text')]")
    REQUIRED_ERROR = (By.XPATH, "//span[text()='Required']")
    REQUIRED_ERRORS = (By.XPATH, "//span[text()='Required']")

    def enter_username(self, username):
        self.type(self.USERNAME, username)

    def enter_password(self, password):
        self.type(self.PASSWORD, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def wait_for_login_page(self):
        self.find_visible_element(self.USERNAME)

    def is_login_error_displayed(self):
        return self.is_element_displayed(self.LOGIN_ERROR)

    def is_login_page_displayed(self):
        return self.is_element_displayed(self.USERNAME)

    def is_required_error_displayed(self):
        return self.is_element_displayed(self.REQUIRED_ERROR)

    def get_required_error_count(self):
        return len(self.find_elements(self.REQUIRED_ERRORS))




