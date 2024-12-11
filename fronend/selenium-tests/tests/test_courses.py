import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage
from pages.courses_page import CoursesPage
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
    """Perform login with the given email."""
    login_page = LoginPage(driver)
    login_page.enter_email(email)
    login_page.click_get_otp()
    time.sleep(2)  # Wait for OTP input field to appear
    otp_input = login_page.get_otp()  # Assuming `get_otp` is implemented to fetch the OTP
    login_page.enter_otp(otp_input)
    login_page.click_validate_otp()
    time.sleep(2)  # Wait for login to complete


# Test: Verify courses page load and title
def test_courses_page_load(driver):
    email = "rey@example.com"
    driver.get('http://localhost:3000/login')
    login(driver, email)
    driver.get('http://localhost:3000/courses')
    assert "Courses" in driver.title

# Test: Verify course list presence
def test_course_list_presence(driver):
    courses_page = CoursesPage(driver)
    courses = courses_page.get_course_list()
    assert len(courses) > 0, "No courses found on courses page"

# Test: Enroll in the first course
def test_enroll_first_course(driver):
    courses_page = CoursesPage(driver)
    course_statuses = courses_page.get_course_status()
    if("Enroll" == course_statuses[0]):
        courses_page.enroll_in_course(0)  # Assuming course IDs start from 0
        time.sleep(2)  # Wait for enrollment to process
        course_statuses = courses_page.get_course_status()
        assert "Enrolled" in course_statuses[0], "Enrollment failed"

# Test: Verify course status updates
def test_verify_course_status(driver):
    courses_page = CoursesPage(driver)
    courses = courses_page.get_course_list()
    assert "Enrolled" in courses[0].find_element(By.CSS_SELECTOR, 'td:last-child').text

    
# Test: Verify search functionality
def test_search_functionality(driver):
    courses_page = CoursesPage(driver)
    search_box = courses_page.get_element(By.NAME, 'search')
    search_box.send_keys("")
    search_box.send_keys("Agile Project Management")
    time.sleep(2)
    search_results = courses_page.get_course_list()
    assert "Agile Project Management" in search_results[0].find_element(By.CSS_SELECTOR, 'td').text
    search_box.clear()
    time.sleep(1)


# Test: Verify course detail navigation
def test_course_detail_navigation(driver):
    driver.get('http://localhost:3000/courses')
    courses_page = CoursesPage(driver)
    course = courses_page.get_course_list()[0]  
    course_title = course.find_element(By.TAG_NAME, 'a')
    course_title.click()
    time.sleep(2)
    assert "CourseDetails" in driver.title
    driver.back()

# Test: Page responsiveness (width check)
def test_responsiveness(driver):
    driver.set_window_size(375, 667)  # Simulate mobile view
    courses_page = CoursesPage(driver)
    assert courses_page.get_element(By.CSS_SELECTOR, '.course-list').is_displayed()


# Test: Verify navigation to home page
def test_navigation_to_home(driver):
    courses_page = CoursesPage(driver)
    home_link = courses_page.get_element(By.LINK_TEXT, 'Home')
    assert home_link.is_displayed()
    home_link.click()
    time.sleep(2)
    assert "Home" in driver.title
    driver.back()

# Test: Validate course duration
def test_validate_course_duration(driver):
    driver.get('http://localhost:3000/courses')
    courses_page = CoursesPage(driver)
    course = courses_page.get_course_list()[0]  
    course_title = course.find_element(By.TAG_NAME, 'a')
    course_title.click()
    course_duration = courses_page.get_element(By.CSS_SELECTOR, 'p.duration')
    assert course_duration.is_displayed() and "hours" in course_duration.text

# Test: Check instructor information presence
def test_instructor_information_presence(driver):
    driver.get('http://localhost:3000/courses')
    courses_page = CoursesPage(driver)
    course = courses_page.get_course_list()[0]  
    course_title = course.find_element(By.TAG_NAME, 'a')
    course_title.click()
    instructor_info = courses_page.get_element(By.CSS_SELECTOR, 'h3')
    assert instructor_info.is_displayed()

def test_pagination(driver):
    """Test the pagination functionality."""
    driver.get('http://localhost:3000/courses')
    courses_page = CoursesPage(driver)
    next_button = courses_page.get_next_button()

    # Wait for the next button to be clickable
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.next'))
    )
    next_button.click()

    time.sleep(2)  # Allow time for the page to load

    prev_button = courses_page.get_prev_button()
    # Ensure the previous button is now displayed
    assert prev_button.is_displayed()


