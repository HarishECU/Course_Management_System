from selenium.webdriver.common.by import By
from .base_page import BasePage

class DashboardPage(BasePage):
    HEADER = (By.CSS_SELECTOR, 'h1')
    COURSE_LIST = (By.CSS_SELECTOR, 'ul.course-list li')
    COURSE_TITLES = (By.CSS_SELECTOR, 'ul.course-list li h3')
    COURSE_DESCRIPTIONS = (By.CSS_SELECTOR, 'ul.course-list li p')
    SEARCH_BOX = (By.NAME, 'search')
    SORT_BUTTON = (By.CSS_SELECTOR, 'button.sort')
    FILTER_DROPDOWN = (By.CSS_SELECTOR, 'select.filter')
    APPLY_BUTTON = (By.CSS_SELECTOR, 'button.apply')
    PAGINATION_BUTTONS = (By.CSS_SELECTOR, '.pagination button')
    COURSE_COUNT = (By.CSS_SELECTOR, '.course-count')
    PROGRESS_BARS = (By.CSS_SELECTOR, '.progress-bar')
    LOGOUT_BUTTON = (By.CSS_SELECTOR, 'button.logout')
    NOTIFICATIONS_PANEL = (By.CSS_SELECTOR, '.notifications')
    NOTIFICATION_MESSAGE = (By.CSS_SELECTOR, '.notifications .message')
    FOOTER = (By.CSS_SELECTOR, 'footer')
    PROFILE_LINK = (By.LINK_TEXT, 'Profile')
    SIDEBAR_TOGGLE = (By.CSS_SELECTOR, 'button.sidebar-toggle')
    SIDEBAR = (By.CSS_SELECTOR, '.sidebar')

    def get_header(self):
        return self.get_element(*self.HEADER)

    def get_course_list(self):
        return self.get_elements(*self.COURSE_LIST)

    def get_course_titles(self):
        return [element.text for element in self.get_elements(*self.COURSE_TITLES)]

    def get_course_descriptions(self):
        return [element.text for element in self.get_elements(*self.COURSE_DESCRIPTIONS)]

    def get_search_box(self):
        return self.get_element(*self.SEARCH_BOX)

    def get_sort_button(self):
        return self.get_element(*self.SORT_BUTTON)

    def get_filter_dropdown(self):
        return self.get_element(*self.FILTER_DROPDOWN)

    def get_apply_button(self):
        return self.get_element(*self.APPLY_BUTTON)

    def get_pagination_buttons(self):
        return self.get_elements(*self.PAGINATION_BUTTONS)

    def get_course_count(self):
        return self.get_element(*self.COURSE_COUNT)

    def get_progress_bars(self):
        return self.get_elements(*self.PROGRESS_BARS)

    def get_logout_button(self):
        return self.get_element(*self.LOGOUT_BUTTON)

    def get_notifications_panel(self):
        return self.get_element(*self.NOTIFICATIONS_PANEL)

    def get_notification_message(self):
        return self.get_element(*self.NOTIFICATION_MESSAGE)

    def get_footer(self):
        return self.get_element(*self.FOOTER)

    def get_profile_link(self):
        return self.get_element(*self.PROFILE_LINK)

    def get_sidebar_toggle(self):
        return self.get_element(*self.SIDEBAR_TOGGLE)

    def get_sidebar(self):
        return self.get_element(*self.SIDEBAR)
