import time
import pytest

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.xlUtils import XLUtils
from utilities.custom_logger import LogGen
from utilities.data_paths import TEST_DATA_PATH


class TestLoginDDT:

    logger = LogGen.loggen()

    file = TEST_DATA_PATH
    sheet = "sheet_one"

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_ddt(self, setup):

        self.logger.info("========== Starting DDT Login Test ==========")

        driver = setup
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        rows = XLUtils.get_row_count(self.file, self.sheet)
        test_results = []

        for r in range(2, rows + 1):

            username = XLUtils.read_data(self.file, self.sheet, r, 1)
            password = XLUtils.read_data(self.file, self.sheet, r, 2)
            expected = XLUtils.read_data(self.file, self.sheet, r, 3)

            self.logger.info(f"Row {r} | Username: {username} | Expected: {expected}")

            # ---------- LOGIN ----------
            login_page.enter_username(username)
            login_page.enter_password(password)
            login_page.click_login()

            time.sleep(2)

            is_dashboard = "dashboard" in driver.current_url.lower()

            # ================= VALID CASE =================
            if expected == "Valid":

                if is_dashboard:
                    self.logger.info("Valid login successful")

                    XLUtils.write_data(self.file, self.sheet, r, 4, "PASS")
                    XLUtils.fill_color(self.file, self.sheet, r, 4, "60b212")
                    test_results.append("PASS")

                    # ---------- LOGOUT ----------
                    dashboard_page.click_logout()

                    login_page.wait_for_login_page()

                else:
                    self.logger.error("Valid login failed")

                    XLUtils.write_data(self.file, self.sheet, r, 4, "FAIL")
                    XLUtils.fill_color(self.file, self.sheet, r, 4, "ff0000")
                    test_results.append("FAIL")

            # ================= INVALID CASE =================
            elif expected == "Invalid":

                if not is_dashboard:
                    self.logger.info("Invalid login correctly failed")

                    XLUtils.write_data(self.file, self.sheet, r, 4, "PASS")
                    XLUtils.fill_color(self.file, self.sheet, r, 4, "60b212")
                    test_results.append("PASS")

                else:
                    self.logger.error("Invalid login but succeeded")

                    XLUtils.write_data(self.file, self.sheet, r, 4, "FAIL")
                    XLUtils.fill_color(self.file, self.sheet, r, 4, "ff0000")
                    test_results.append("FAIL")

                    dashboard_page.click_logout()

                    login_page.wait_for_login_page()

        self.logger.info("========== DDT Login Test Completed ==========")

        # ---------- FINAL ASSERTION ----------
        assert "FAIL" not in test_results
