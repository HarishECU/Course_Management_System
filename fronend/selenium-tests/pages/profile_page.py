from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class ProfilePage(BasePage):
    USER_NAME = (By.CSS_SELECTOR, '.user-profile p:nth-of-type(1)')
    USER_EMAIL = (By.CSS_SELECTOR, '.user-profile p:nth-of-type(2)')
    COURSES_ENROLLED = (By.CSS_SELECTOR, '.user-profile p:nth-of-type(3)')
    ERROR_MESSAGE = (By.CSS_SELECTOR, 'p')

    def get_user_name(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.USER_NAME)
        )
        return self.get_element(*self.USER_NAME).text

    def get_user_email(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.USER_EMAIL)
        )
        return self.get_element(*self.USER_EMAIL).text

    def get_courses_enrolled(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.COURSES_ENROLLED)
        )
        return self.get_element(*self.COURSES_ENROLLED).text

    def get_error_message(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.ERROR_MESSAGE)
        )
        return self.get_element(*self.ERROR_MESSAGE).text
