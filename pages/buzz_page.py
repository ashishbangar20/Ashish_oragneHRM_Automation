from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class BuzzPage(BasePage):

    BUZZ_MENU = (By.XPATH, "//span[text()='Buzz']")
    POST_TEXT_AREA = (By.XPATH, "//textarea[contains(@class,'oxd-buzz-post-input')]")
    POST_BUTTON = (By.XPATH, "//button[@type='submit']")
    POST_CONTAINER = (By.XPATH, "//div[contains(@class,'orangehrm-buzz-newsfeed-posts')]")
    LATEST_POST = (By.XPATH, "//div[contains(@class,'orangehrm-buzz-post-body')]//p[1]")

    def click_buzz_menu(self):
        self.click(self.BUZZ_MENU)

    def enter_post_message(self, message):
        self.type(self.POST_TEXT_AREA, message)

    def click_post_button(self):
        self.click(self.POST_BUTTON)

    def post_message(self, message):
        self.enter_post_message(message)
        self.click_post_button()

        # Wait until textarea clears (post submitted)
        self.wait.until(
            lambda driver:
            self.get_attribute(self.POST_TEXT_AREA, "value") == ""
        )

    def is_post_present(self, message):
        try:
            self.find_element(self.POST_CONTAINER)
            latest_post_text = self.get_text(self.LATEST_POST)
            return message.strip() == latest_post_text.strip()
        except Exception as e:
            print(e)
            return False
