from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DashboardPage:

    DASHBOARD_MENU = (By.XPATH, "//span[text()='Dashboard']")
    PROFILE_ICON = (By.XPATH, "//span[@class='oxd-userdropdown-tab']")
    LOGOUT_BTN = (By.XPATH, "//a[text()='Logout']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)   # ✅ Common wait

    def click_logout(self):

        self.wait.until(EC.element_to_be_clickable(self.PROFILE_ICON)).click()
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_BTN)).click()

    def wait_for_dashboard_menu(self):

        self.wait.until(EC.presence_of_element_located(self.DASHBOARD_MENU))

