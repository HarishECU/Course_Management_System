import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pages.register_page import RegisterPage
import sys
import os

# Add the parent directory of 'tests' to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome(service=Service(executable_path='tests/chromedriver.exe'))
    driver.get('http://localhost:3000/register')
    yield driver
    driver.quit()

# Test 1: Page Load
def test_page_load(driver):
    driver.get('http://localhost:3000/register')
    assert "Register" in driver.title

# Test 2: Verify name input field presence
def test_name_input_presence(driver):
    register_page = RegisterPage(driver)
    name_input = register_page.get_element(By.NAME, 'name')
    assert name_input.is_displayed()

# Test 3: Verify email input field presence
def test_email_input_presence(driver):
    register_page = RegisterPage(driver)
    email_input = register_page.get_element(By.NAME, 'email')
    assert email_input.is_displayed()

# Test 4: Verify register button presence
def test_register_button_presence(driver):
    register_page = RegisterPage(driver)
    register_button = register_page.get_element(By.CSS_SELECTOR, 'button[type="submit"]')
    assert register_button.is_displayed()

# Test 5: Check name validation
def test_name_validation(driver):
    register_page = RegisterPage(driver)
    register_page.enter_name("")
    register_page.enter_email("test@example.com")
    register_page.click_register()
    time.sleep(1)
    error_message = register_page.wait_for_element(By.CSS_SELECTOR, 'p.error')
    assert "Name is required" in error_message.text

# Test 6: Check email validation
def test_email_validation(driver):
    driver.get('http://localhost:3000/register')
    register_page = RegisterPage(driver)
    register_page.enter_name("Test User")
    register_page.click_register()
    time.sleep(1)
    error_message = register_page.wait_for_element(By.CSS_SELECTOR, 'p.error')
    assert "Email is required" in error_message.text

# Test 10: Check email format validation
def test_email_format_validation(driver):
    register_page = RegisterPage(driver)
    register_page.enter_name("Test User")
    register_page.enter_email("invalid-email")
    register_page.click_register()
    time.sleep(1)
    error_message = register_page.get_element(By.NAME, 'email').get_attribute('validationMessage')
    assert "Please include an '@' in the email address. 'invalid-email' is missing an '@'." in error_message or "please enter a valid email address" in error_message

# Test 11: Check registration button state
def test_register_button_state(driver):
    register_page = RegisterPage(driver)
    register_page.enter_name("Test User")
    register_page.enter_email("test@example.com")
    register_button = register_page.get_element(By.CSS_SELECTOR, 'button[type="submit"]')
    assert register_button.is_enabled()

# Test 12: Verify existing user error
def test_existing_user_error(driver):
    driver.get('http://localhost:3000/register')
    register_page = RegisterPage(driver)
    register_page.enter_name("Test User")
    register_page.enter_email("pia@example.com")
    register_page.click_register()
    time.sleep(1)
    error_message = register_page.wait_for_element(By.CSS_SELECTOR, 'p.error')
    assert "Email already exists" in error_message.text

# Test 13: Check registration form responsiveness (width check)
def test_registration_form_responsiveness(driver):
    register_page = RegisterPage(driver)
    driver.set_window_size(375, 667)  # Simulate mobile view
    assert register_page.get_element(By.NAME, 'name').is_displayed()

# Test 14: Verify navigation to login page
def test_navigation_to_login(driver):
    register_page = RegisterPage(driver)
    login_link = register_page.get_element(By.LINK_TEXT, 'Login')
    assert login_link.is_displayed()
    login_link.click()
    time.sleep(2)
    assert "Login" in driver.title
    driver.back()


# Test 15: Validate empty form submission
def test_empty_form_submission(driver):    
    driver.get('http://localhost:3000/register')
    register_page = RegisterPage(driver)
    register_page.click_register()
    time.sleep(1)
    error_message = register_page.wait_for_element(By.CSS_SELECTOR, 'p.error')
    assert "All fields are required" in error_message.text
