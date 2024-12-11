import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
import random 
import sys
import os

# Add the parent directory of 'tests' to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome(service=Service(executable_path='tests/chromedriver.exe'))
    yield driver
    driver.quit()

def login(driver, email):
    login_page = LoginPage(driver)
    login_page.enter_email(email)
    login_page.click_get_otp()
    time.sleep(2)  # Wait for OTP input field to appear
    otp_input = login_page.get_otp()  # Assuming `get_otp` is implemented to fetch the OTP
    login_page.enter_otp(otp_input)
    login_page.click_validate_otp()
    time.sleep(2)  # Wait for login to complete

# Test: Verify page load and title
def test_page_load(driver):
    email = "dcba@gmail.com"
    driver.get('http://localhost:3000/login')
    login(driver, email)
    driver.get('http://localhost:3000/dashboard')
    dashboard_page = DashboardPage(driver)

    assert "Dashboard" in driver.title

# Test: Verify dashboard header presence
def test_dashboard_header_presence(driver):
    dashboard_page = DashboardPage(driver)
    header = dashboard_page.get_header()
    assert header.is_displayed() and "Dashboard" in header.text

# Test: Verify course list presence
def test_course_list_presence(driver):
    dashboard_page = DashboardPage(driver)
    courses = dashboard_page.get_course_list()
    assert len(courses) > 0, "No courses found on dashboard"

# Test: Verify course titles and descriptions
def test_course_titles_and_descriptions(driver):
    dashboard_page = DashboardPage(driver)
    course_titles = dashboard_page.get_course_titles()
    course_descriptions = dashboard_page.get_course_descriptions()
    assert all(title != "" for title in course_titles), "Some course titles are empty"
    assert all(description != "" for description in course_descriptions), "Some course descriptions are empty"

# Test: Check navigation to course details
def test_navigation_to_course_details(driver):
    dashboard_page = DashboardPage(driver)
    course = dashboard_page.get_course_list()[0]
    course_title = course.find_element(By.TAG_NAME, 'a')
    course_title.click()
    time.sleep(2)
    assert "CourseDetails" in driver.title
    driver.back()

# Test: Check search functionality
def test_search_functionality(driver):
    dashboard_page = DashboardPage(driver)
    search_box = dashboard_page.get_search_box()
    sc = random.choice(dashboard_page.get_course_titles())
    search_box.send_keys(sc)
    time.sleep(2)
    search_results = dashboard_page.get_course_titles()
    assert sc in search_results

# Test: Check filters functionality
def test_filters_functionality(driver):
    dashboard_page = DashboardPage(driver)
    filter_dropdown = dashboard_page.get_filter_dropdown()
    filter_dropdown.click()
    filter_option = filter_dropdown.find_element(By.XPATH, '//option[@value="Active"]')
    filter_option.click()
    apply_button = dashboard_page.get_apply_button()
    apply_button.click()
    time.sleep(2)
    filtered_courses = dashboard_page.get_course_list()
    assert len(filtered_courses) == 0, "No courses found with filter applied"

# Test: Verify course progress
def test_course_progress(driver):
    dashboard_page = DashboardPage(driver)
    course_progress = dashboard_page.get_progress_bars()
    assert all(int(progress.get_attribute("value")) <= 100 for progress in course_progress)

# Test: Test responsiveness (width check)
def test_responsiveness(driver):
    driver.set_window_size(375, 667)  # Simulate mobile view
    dashboard_page = DashboardPage(driver)
    assert dashboard_page.get_element(By.CSS_SELECTOR, '.dashboard').is_displayed()

# Test: Check course pagination (if applicable)
def test_course_pagination(driver):
    dashboard_page = DashboardPage(driver)
    next_button = dashboard_page.get_element(By.CSS_SELECTOR, 'button.next')
    if next_button.is_displayed():
        next_button.click()
        time.sleep(2)
        assert dashboard_page.get_element(By.CSS_SELECTOR, 'button.prev').is_displayed()

# Test: Verify page load speed
def test_page_load_speed(driver):
    start_time = time.time()
    driver.refresh()
    load_time = time.time() - start_time
    assert load_time < 5, f"Page load time is too high: {load_time} seconds"

# Test: Verify footer presence
def test_footer_presence(driver):
    dashboard_page = DashboardPage(driver)
    footer = dashboard_page.get_footer()
    assert footer.is_displayed()

# Test: Verify course list sorting
def test_course_list_sorting(driver):
    dashboard_page = DashboardPage(driver)
    sort_button = dashboard_page.get_sort_button()
    sort_button.click()
    sorted_courses = dashboard_page.get_course_titles()
    assert sorted_courses == sorted(sorted_courses), "Courses are not sorted correctly"

# Test: Check notifications panel presence
def test_notifications_panel_presence(driver):
    dashboard_page = DashboardPage(driver)
    notifications_panel = dashboard_page.get_notifications_panel()
    assert notifications_panel.is_displayed()

# Test: Verify notification message for a new course
def test_notification_message(driver):
    dashboard_page = DashboardPage(driver)
    notification_message = dashboard_page.get_notification_message()
    assert "New course added" in notification_message.text
