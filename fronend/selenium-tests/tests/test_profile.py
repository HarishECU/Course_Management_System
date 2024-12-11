import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
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
    

def test_user_profile_page_load(driver):
    """Test if the Profile page loads correctly."""
    email = "rey@example.com"
    driver.get('http://localhost:3000/login')
    login(driver, email)
    driver.get('http://localhost:3000/profile')
    assert "Profile" in driver.title

def test_user_name_display(driver):
    """Test if the user's name is displayed correctly."""
    profile_page = ProfilePage(driver)
    user_name = profile_page.get_user_name()
    assert user_name != "", "User name is not displayed"

def test_user_email_display(driver):
    """Test if the user's email is displayed correctly."""
    profile_page = ProfilePage(driver)
    user_email = profile_page.get_user_email()
    assert user_email != "", "User email is not displayed"

def test_courses_enrolled_display(driver):
    """Test if the number of courses enrolled is displayed correctly."""
    profile_page = ProfilePage(driver)
    courses_enrolled = profile_page.get_courses_enrolled()
    assert "Courses Enrolled: " in courses_enrolled, "Courses enrolled count is not displayed correctly"
