import os


def capture_screenshot(driver, test_name):

    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    driver.save_screenshot(f"screenshots/{test_name}.png")
