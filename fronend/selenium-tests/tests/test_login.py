import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage
import sys
import os

# Add the parent directory of 'tests' to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome(service=Service(executable_path='tests/chromedriver.exe'))
    driver.get('http://localhost:3000/login')
    yield driver
    driver.quit()

def test_page_load(driver):
    login_page = LoginPage(driver)
    
    time.sleep(2)  # Wait for 2 seconds to ensure the page is fully loaded
    assert "Login" in driver.title

def test_email_input_presence(driver):
    login_page = LoginPage(driver)
    
    email_input = login_page.wait_for_element(By.NAME, 'email')
    assert email_input.is_displayed()

def test_get_otp_button_presence(driver):
    login_page = LoginPage(driver)
    
    get_otp_button = login_page.wait_for_element(By.CSS_SELECTOR, 'button[type="submit"]')
    assert get_otp_button.is_displayed()

def test_generate_otp(driver):
    login_page = LoginPage(driver)
    
    login_page.enter_email("pia@example.com")
    login_page.click_get_otp()
    time.sleep(2)  # Wait for OTP generation

def test_otp_input_presence(driver):
    login_page = LoginPage(driver)
    
    otp_input = login_page.wait_for_element(By.NAME, 'otp')
    assert otp_input.is_displayed()

def test_invalid_otp(driver):
    login_page = LoginPage(driver)
    
    login_page.enter_otp("123456")
    login_page.click_validate_otp()
    error_message = login_page.wait_for_element(By.CSS_SELECTOR, 'p.error')
    assert "Invalid OTP or user not found" in error_message.text

def test_invalid_email(driver):
    driver.get("http://localhost:3000/login")
    login_page = LoginPage(driver)
    
    login_page.enter_email("invalid@example.com")
    login_page.click_get_otp()
    error_message = login_page.wait_for_element(By.CSS_SELECTOR, 'p.error')
    assert "Email not found" in error_message.text

def test_otp_resend(driver):
    login_page = LoginPage(driver)
    
    login_page.enter_email("abcd@gmail.com")
    login_page.click_get_otp()
    time.sleep(2)
    login_page.click_get_otp()
    success_message = login_page.wait_for_element(By.CSS_SELECTOR, 'p.success')
    assert "OTP sent successfully" in success_message.text

def test_page_responsiveness(driver):
    driver.get("http://localhost:3000/login")
    login_page = LoginPage(driver)
    
    driver.set_window_size(375, 667)  # Simulate mobile view
    assert login_page.get_element(By.NAME, 'email').is_displayed()

def test_email_format_validation(driver):
    login_page = LoginPage(driver)
    
    login_page.enter_email("invalid-email")
    email_input = login_page.get_element(By.NAME, 'email')
    validation_message = email_input.get_attribute('validationMessage')
    assert "Please include an '@' in the email address. 'invalid-email' is missing an '@'." in validation_message or "please enter a valid email address" in validation_message.lower()

def test_empty_email_submission(driver):
    login_page = LoginPage(driver)
    
    login_page.enter_email("")
    get_otp_button = login_page.get_element(By.CSS_SELECTOR, 'button[type="submit"]')
    get_otp_button.click()
    email_input = login_page.get_element(By.NAME, 'email')
    validation_message = email_input.get_attribute('validationMessage')
    assert validation_message == "Please fill out this field."

def test_empty_otp_submission(driver):
    driver.get("http://localhost:3000/login")
    login_page = LoginPage(driver)
    
    login_page.enter_email("pia@example.com")
    login_page.click_get_otp()
    time.sleep(2)
    login_page.click_validate_otp()
    otp_input = login_page.wait_for_element(By.NAME, 'otp')
    validation_message = otp_input.get_attribute('validationMessage')
    assert validation_message == "Please fill out this field."
