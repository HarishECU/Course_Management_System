from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Utils:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
            return element
        except TimeoutException:
            print(f"Element with locator ({by}, {value}) not found within {timeout} seconds")
            return None

    def wait_for_clickable(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, value)))
            return element
        except TimeoutException:
            print(f"Element with locator ({by}, {value}) not clickable within {timeout} seconds")
            return None

    def take_screenshot(self, file_path):
        self.driver.save_screenshot(file_path)

    def click_element(self, by, value):
        element = self.wait_for_clickable(by, value)
        if element:
            element.click()
        else:
            print(f"Element with locator ({by}, {value}) not clickable")

    def send_keys_to_element(self, by, value, keys):
        element = self.wait_for_element(by, value)
        if element:
            element.clear()
            element.send_keys(keys)
        else:
            print(f"Element with locator ({by}, {value}) not found")

    def get_element_text(self, by, value):
        element = self.wait_for_element(by, value)
        if element:
            return element.text
        else:
            print(f"Element with locator ({by}, {value}) not found")
            return ""
