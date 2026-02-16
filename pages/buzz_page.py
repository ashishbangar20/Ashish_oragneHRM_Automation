from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BuzzPage:

    buzz_menu = (By.XPATH, "//span[text()='Buzz']")
    post_text_area = (By.XPATH, "//textarea[contains(@class,'oxd-buzz-post-input')]")
    post_button = (By.XPATH, "//button[@type='submit']")
    post_texts = (By.XPATH, "//div[contains(@class,'oxd-buzz-post-body')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click_buzz_menu(self):
        self.wait.until(EC.element_to_be_clickable(self.buzz_menu)).click()

    def enter_post_message(self, message):
        self.wait.until(EC.visibility_of_element_located(self.post_text_area)).send_keys(message)

    def click_post_button(self):
        self.wait.until(EC.element_to_be_clickable(self.post_button)).click()

    def is_post_present(self, message):
        try:
            # Wait for post list to refresh
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class,'orangehrm-buzz-newsfeed-posts')]")
                )
            )

            # Always check latest post (top one)
            latest_post = self.driver.find_element(
                By.XPATH,
                "(//div[contains(@class,'oxd-buzz-post')]//p)[1]"
            )

            print("Latest Post Text:", latest_post.text)

            return message.strip() == latest_post.text.strip()

        except Exception as e:
            print("Exception while validating post:", e)
            return False

