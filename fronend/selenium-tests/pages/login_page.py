from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    EMAIL_INPUT = (By.NAME, 'email')
    OTP_INPUT = (By.NAME, 'otp')
    GET_OTP_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    VALIDATE_OTP_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    MESSAGE = (By.CSS_SELECTOR, 'p.error, p.success')  # To handle both error and success messages

    def enter_email(self, email):
        self.send_keys_to_element(*self.EMAIL_INPUT, email)

    def enter_otp(self, otp):
        self.send_keys_to_element(*self.OTP_INPUT, otp)

    def click_get_otp(self):
        self.click_element(*self.GET_OTP_BUTTON)

    def click_validate_otp(self):
        self.click_element(*self.VALIDATE_OTP_BUTTON)

    def get_message(self):
        return self.get_element(*self.MESSAGE).text
    def get_otp(self):
        return self.get_element(By.CSS_SELECTOR, 'p.success, p.error').get_attribute('name')