import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, StaleElementReferenceException,ElementClickInterceptedException,)

class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # CORE FIND METHODS
    def find_element(self, locator):
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise Exception(f"Element not found: {locator}")

    def find_elements(self, locator):
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []

    def find_visible_element(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise Exception(f"Element not visible: {locator}")

    # WAIT METHODS
    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_loader(self, loader_locator):
        WebDriverWait(self.driver, 20).until(
            EC.invisibility_of_element_located(loader_locator))

    # ACTION METHODS
    def click(self, locator):
        self.wait_for_clickable(locator).click()

    def safe_click(self, locator, retries=3):
        for _ in range(retries):
            try:
                self.wait_for_clickable(locator).click()
                return
            except (StaleElementReferenceException,
                    ElementClickInterceptedException):
                time.sleep(1)
        raise Exception(f"Failed to click after {retries} attempts: {locator}")

    def js_click(self, locator):
        element = self.find_visible_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text):
        element = self.find_visible_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_visible_element(locator).text

    def get_attribute(self, locator, attribute):
        return self.find_visible_element(locator).get_attribute(attribute)

    # DROPDOWN
    def select_by_visible_text(self, locator, text):
        Select(self.find_visible_element(locator)).select_by_visible_text(text)

    def select_by_value(self, locator, value):
        Select(self.find_visible_element(locator)).select_by_value(value)

    def select_by_index(self, locator, index):
        Select(self.find_visible_element(locator)).select_by_index(index)

    # UTILITIES
    def is_element_displayed(self, locator):
        try:
            return self.find_visible_element(locator).is_displayed()
        except:
            return False

    def is_element_enabled(self, locator):
        try:
            return self.find_visible_element(locator).is_enabled()
        except:
            return False

    def is_element_selected(self, locator):
        try:
            return self.find_visible_element(locator).is_selected()
        except:
            return False

    def scroll_to_element(self, locator):
        element = self.find_visible_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element)

    def scroll_to_bottom(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

    # IFRAME
    def switch_to_frame_by_locator(self, locator):
        self.driver.switch_to.frame(self.find_element(locator))

    def switch_to_frame_by_name(self, name):
        self.driver.switch_to.frame(name)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    # WINDOW
    def switch_to_new_window(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def switch_to_window_by_index(self, index):
        self.driver.switch_to.window(self.driver.window_handles[index])

    def close_current_window(self):
        self.driver.close()

    def switch_to_main_window(self):
        self.driver.switch_to.window(self.driver.window_handles[0])

    # ACTION CHAINS
    def hover(self, locator):
        ActionChains(self.driver).move_to_element(
            self.find_visible_element(locator)).perform()

    def double_click(self, locator):
        ActionChains(self.driver).double_click(
            self.find_visible_element(locator)).perform()

    def right_click(self, locator):
        ActionChains(self.driver).context_click(
            self.find_visible_element(locator)).perform()

    def drag_and_drop(self, source, target):
        ActionChains(self.driver).drag_and_drop(
            self.find_visible_element(source),
            self.find_visible_element(target)).perform()

    def click_and_hold(self, locator):
        ActionChains(self.driver).click_and_hold(
            self.find_visible_element(locator)).perform()

    def release(self, locator):
        ActionChains(self.driver).release(
            self.find_visible_element(locator)).perform()

    def press_key(self, locator, key):
        self.find_visible_element(locator).send_keys(key)

    def press_enter(self, locator):
        self.find_visible_element(locator).send_keys(Keys.ENTER)


    # ASSERTION
    def assert_element_text(self, locator, expected):
        actual = self.get_text(locator)
        assert actual == expected, \
            f"Expected '{expected}', but got '{actual}'"
