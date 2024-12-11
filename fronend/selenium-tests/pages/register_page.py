from selenium.webdriver.common.by import By
from .base_page import BasePage

class RegisterPage(BasePage):
    NAME_INPUT = (By.NAME, 'name')
    EMAIL_INPUT = (By.NAME, 'email')
    REGISTER_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    MESSAGE = (By.CSS_SELECTOR, 'p')

    def enter_name(self, name):
        self.send_keys_to_element(*self.NAME_INPUT, name)

    def enter_email(self, email):
        self.send_keys_to_element(*self.EMAIL_INPUT, email)

    def click_register(self):
        self.click_element(*self.REGISTER_BUTTON)

    def get_message(self):
        return self.get_element(*self.MESSAGE).text
