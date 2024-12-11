import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.courses_page import CoursesPage

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome(executable_path='selenium-tests/drivers/chromedriver')
    driver.get("http://localhost:3000/courses')
    yield driver
    driver.quit()

def test_courses(driver):
    courses_page = CoursesPage(driver)

    # Test 1: Page Load
    assert "Courses" in driver.title

    # Test 2: Verify course list presence
    courses = courses_page.get_course_list()
    assert len(courses) > 0, "No courses found on courses page"

    # Test 3: Enroll in the first course
    courses_page.enroll_in_course(0)  # Assuming course IDs start from 0
    time.sleep(2)  # Wait for enrollment to process
    course_statuses = courses_page.get_course_status()
    assert "Enrolled" in course_statuses[0], "Enrollment failed"

    # Test 4: Verify course status updates
    courses = courses_page.get_course_list()
    assert "Enrolled" in courses[0].find_element(By.CSS_SELECTOR, 'td:last-child').text

    # Test 5: Check pagination (if applicable)
    next_button = courses_page.get_element(By.CSS_SELECTOR, 'button.next')
    if next_button.is_displayed():
        next_button.click()
        time.sleep(2)
        assert courses_page.get_element(By.CSS_SELECTOR, 'button.prev').is_displayed()

    # Test 6: Verify search functionality
    search_box = courses_page.get_element(By.NAME, 'search')
    search_box.send_keys("Course Title")
    search_box.submit()
    time.sleep(2)
    search_results = courses_page.get_course_list()
    assert "Course Title" in search_results[0].find_element(By.CSS_SELECTOR, 'td').text

    # Test 7: Verify filter functionality
    filter_button = courses_page.get_element(By.CSS_SELECTOR, 'button.filter')
    filter_button.click()
    filter_option = courses_page.get_element(By.CSS_SELECTOR, 'option[value="Active"]')
    filter_option.click()
    apply_button = courses_page.get_element(By.CSS_SELECTOR, 'button.apply')
    apply_button.click()
    time.sleep(2)
    filtered_courses = courses_page.get_course_list()
    assert len(filtered_courses) > 0, "No courses found with filter applied"

    # Test 8: Verify course detail navigation
    course = courses_page.get_course_list()[0]
    course.click()
    time.sleep(2)
    assert "Course Details" in driver.title
    driver.back()

    # Test 9: Check course progress tracking
    progress = courses_page.get_element(By.CSS_SELECTOR, '.course-progress')
    assert progress.is_displayed()

    # Test 10: Page responsiveness (width check)
    driver.set_window_size(375, 667)  # Simulate mobile view
    assert courses_page.get_element(By.CSS_SELECTOR, '.course-list').is_displayed()

    # Test 11: Verify course list sorting
    sort_button = courses_page.get_element(By.CSS_SELECTOR, 'button.sort')
    sort_button.click()
    sorted_courses = courses_page.get_course_titles()
    assert sorted_courses == sorted(sorted_courses), "Courses are not sorted correctly"

    # Test 12: Check notifications panel presence
    notifications_panel = courses_page.get_element(By.CSS_SELECTOR, '.notifications')
    assert notifications_panel.is_displayed()

    # Test 13: Verify notification message for a new course
    notification_message = courses_page.get_element(By.CSS_SELECTOR, '.notifications .message')
    assert "New course added" in notification_message.text

    # Test 14: Verify navigation to home page
    home_link = courses_page.get_element(By.LINK_TEXT, 'Home')
    assert home_link.is_displayed()
    home_link.click()
    time.sleep(2)
    assert "Home" in driver.title
    driver.back()

    # Test 15: Validate course duration
    course_duration = courses_page.get_element(By.CSS_SELECTOR, '.course-duration')
    assert course_duration.is_displayed() and "hours" in course_duration.text

    # Test 16: Check instructor information presence
    instructor_info = courses_page.get_element(By.CSS_SELECTOR, '.instructor-info')
    assert instructor_info.is_displayed()

    # Test 17: Verify enroll button state for enrolled courses
    enrolled_button = courses_page.get_element(By.CSS_SELECTOR, 'td:last-child button')
    assert enrolled_button.is_displayed() and "Enrolled" in enrolled_button.text

    # Test 18: Validate enrollment for multiple courses
    for i in range(1, 3):
        courses_page.enroll_in_course(i)  # Enroll in second and third courses
        time.sleep(2)
    course_statuses = courses_page.get_course_status()
    assert all("Enrolled" in status for status in course_statuses[:3]), "Enrollment failed for multiple courses"

    # Test 19: Verify unenroll functionality (if applicable)
    unenroll_button = courses_page.get_element(By.CSS_SELECTOR, 'button.unenroll')
    if unenroll_button.is_displayed():
        unenroll_button.click()
        time.sleep(2)
        assert "Enroll" in unenroll_button.text, "Unenrollment failed"

    # Test 20: Validate course ratings presence
    course_ratings = courses_page.get_element(By.CSS_SELECTOR, '.course-rating')
    assert course_ratings.is_displayed() and "stars" in course_ratings.text
