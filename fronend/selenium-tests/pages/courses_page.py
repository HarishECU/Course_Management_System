from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class CoursesPage(BasePage):
    COURSE_LIST = (By.CSS_SELECTOR, 'tbody tr')
    ENROLL_BUTTON = (By.CSS_SELECTOR, 'tbody tr button')
    COURSE_STATUS = (By.CSS_SELECTOR, 'td:last-child')
    SEARCH_BOX = (By.NAME, 'search')
    FILTER_DROPDOWN = (By.CSS_SELECTOR, 'select.filter')
    SORT_BUTTON = (By.CSS_SELECTOR, 'button.sort')
    NEXT_BUTTON = (By.CSS_SELECTOR, 'button.next')
    PREV_BUTTON = (By.CSS_SELECTOR, 'button.prev')
    COURSE_COUNT = (By.CSS_SELECTOR, '.course-count')
    APPLY_BUTTON = (By.CSS_SELECTOR, 'button.apply')
    MESSAGE = (By.CSS_SELECTOR, 'p')
    HOME_LINK = (By.LINK_TEXT, 'Home')
    COURSE_DURATION = (By.CSS_SELECTOR, '.course-duration')
    INSTRUCTOR_INFO = (By.CSS_SELECTOR, '.instructor-info')
    UNENROLL_BUTTON = (By.CSS_SELECTOR, 'button.unenroll')
    COURSE_RATINGS = (By.CSS_SELECTOR, '.course-rating')

    def get_course_list(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.COURSE_LIST)
        )
        return self.get_elements(*self.COURSE_LIST)

    def enroll_in_course(self, course_index):
        enroll_buttons = self.get_elements(*self.ENROLL_BUTTON)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'tbody tr:nth-child({course_index + 1}) button'))
        )
        enroll_buttons[course_index].click()

    def get_course_status(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.COURSE_STATUS)
        )
        return [course.find_element(By.CSS_SELECTOR, 'td:last-child').text for course in self.get_elements(*self.COURSE_LIST)]

    def get_search_box(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SEARCH_BOX)
        )
        return self.get_element(*self.SEARCH_BOX)

    def get_filter_dropdown(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.FILTER_DROPDOWN)
        )
        return self.get_element(*self.FILTER_DROPDOWN)

    def get_sort_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SORT_BUTTON)
        )
        return self.get_element(*self.SORT_BUTTON)

    def get_next_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.NEXT_BUTTON)
        )
        return self.get_element(*self.NEXT_BUTTON)

    def get_prev_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.PREV_BUTTON)
        )
        return self.get_element(*self.PREV_BUTTON)

    def get_course_count(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.COURSE_COUNT)
        )
        return self.get_element(*self.COURSE_COUNT)

    def get_apply_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.APPLY_BUTTON)
        )
        return self.get_element(*self.APPLY_BUTTON)

    def get_message(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.MESSAGE)
        )
        return self.get_element(*self.MESSAGE)

    def get_course_titles(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.COURSE_LIST)
        )
        return [course.find_element(By.CSS_SELECTOR, 'td:first-child').text for course in self.get_elements(*self.COURSE_LIST)]

    def get_home_link(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.HOME_LINK)
        )
        return self.get_element(*self.HOME_LINK)

    def get_course_duration(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.COURSE_DURATION)
        )
        return self.get_element(*self.COURSE_DURATION)

    def get_instructor_info(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.INSTRUCTOR_INFO)
        )
        return self.get_element(*self.INSTRUCTOR_INFO)

    def get_unenroll_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.UNENROLL_BUTTON)
        )
        return self.get_element(*self.UNENROLL_BUTTON)

    def get_course_ratings(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.COURSE_RATINGS)
        )
        return self.get_element(*self.COURSE_RATINGS)
