Backend Project for Course Management System
============================================

This backend project is designed to manage users, courses, and enrollments for an online course management system. The project is built using Flask and provides various RESTful API endpoints to handle user authentication, course details, enrollments, and more.

Project Structure
-----------------
project/
├── data/
│   ├── users.json
│   ├── courses.json
│   ├── enrollments.json
├── src/
│   ├── models.py
│   ├── routes.py
│   ├── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_routes.py
├── .env
├── config.py
├── requirements.txt
├── run.py

Installation
------------
1. Clone the Repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
2. Create a Virtual Environment:
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install Dependencies:
   pip install -r requirements.txt




Running the Application
-------------------------

Set Up Environment Variables: Create a .env file in the root directory and add the necessary environment variables.

Start the Flask Application:
	flask run


API Endpoints
-------------

1. Generate OTP:
POST /api/user/generate-otp
Body: { "email": "user@example.com" }

2.Login:
POST /api/login
Body: { "email": "user@example.com", "otp": "123456" }

3.Logout:
POST /api/logout

4.User Profile:
GET /api/user/profile

5.Register User:
POST /api/user/register
Body: { "name": "New User", "email": "new.user@example.com" }

6.Get All Courses:
GET /api/courses

7.Get Course Details:
GET /api/course/<int:id>



Running Tests
--------------



Run Unit Tests
--------------
Use the pytest command to run all tests:
pytest


Generate Code Coverage Report
-----------------------------
Run Tests with Coverage:
coverage run -m pytest

Generate HTML Report:
coverage html

View the Report:
open htmlcov/index.html  # On macOS
start htmlcov/index.html  # On Windows
xdg-open htmlcov/index.html  # On Linux



other way to Run unit tests:-
python -m coverage run -m unittest discover -s tests
python -m coverage report
python -m coverage html
