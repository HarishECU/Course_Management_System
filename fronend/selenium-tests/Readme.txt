# Selenium Test Suite for Web Application

This test suite contains end-to-end test cases for the web application. It covers various functionalities including login, dashboard, courses, profile, and registration pages.


## Test Scripts Overview

1. **config.json**: Contains configuration details such as base URL and credentials.
2. **drivers**: Directory to store browser drivers (e.g., ChromeDriver).
3. **pages**: Contains Page Object Model (POM) classes for different pages.
    - **base_page.py**: Base class for all page objects.
    - **login_page.py**: Page object class for the login page.
    - **dashboard_page.py**: Page object class for the dashboard page.
    - **courses_page.py**: Page object class for the courses page.
    - **profile_page.py**: Page object class for the profile page.
    - **register_page.py**: Page object class for the registration page.
4. **tests**: Contains test scripts for different functionalities.
    - **test_login.py**: Tests for login functionality.
    - **test_dashboard.py**: Tests for dashboard functionality.
    - **test_courses.py**: Tests for courses functionality.
    - **test_profile.py**: Tests for profile functionality.
    - **test_register.py**: Tests for registration functionality.
5. **utils**: Contains utility functions for common tasks in the test scripts.
    - **utils.py**: Utility functions for waiting for elements, taking screenshots, etc.
6. **conftest.py**: Defines common fixtures for the tests.
7. **requirements.txt**: Lists the dependencies required to run the tests.
8. **run_tests.py**: Script to run the tests using pytest.

## How to Run the Tests

1. **Install Dependencies**:
   Ensure you have Python and pip installed. Navigate to the `selenium-tests` directory and run:
        pip install -r requirements.txt



2. **Download and Configure WebDriver**:
Download the appropriate WebDriver for your browser (e.g., ChromeDriver) and place it in the `drivers` directory.

3. **Run the Tests**:
Execute the test suite by running the `run_tests.py` script:
    python run_tests.py



This will run all the test cases and provide a detailed output of the test results.

## Notes
- Ensure the web application is running at the specified base URL in `config/config.json`.
- Update the credentials and other configuration details in `config/config.json` as needed.
- You can customize and extend the test cases as per your requirements.

For any issues or further assistance, feel free to reach out!
