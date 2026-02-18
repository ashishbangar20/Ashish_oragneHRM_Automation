from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):

    DASHBOARD_MENU = (By.XPATH, "//span[text()='Dashboard']")
    PROFILE_ICON = (By.XPATH, "//span[@class='oxd-userdropdown-tab']")
    LOGOUT_BTN = (By.XPATH, "//a[text()='Logout']")

    def wait_for_dashboard_menu(self):
        self.find_visible_element(self.DASHBOARD_MENU)

    def click_logout(self):
        self.click(self.PROFILE_ICON)
        self.click(self.LOGOUT_BTN)

    def is_dashboard_displayed(self):
        return self.is_element_displayed(self.DASHBOARD_MENU)



