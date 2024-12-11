import unittest
from unittest.mock import patch
from flask import Flask
import sys
import os

# Add the parent directory of 'app' to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.routes import main_blueprint, users, courses, enrollments, otps, session,send_email

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'test_secret_key'
        self.app.register_blueprint(main_blueprint)
        self.client = self.app.test_client()

    def test_get_user_profile_not_logged_in(self):
        with self.app.test_request_context():
            session['user_id'] = None
            response = self.client.get('/api/user/profile')
            self.assertEqual(response.status_code, 401)
            self.assertIn('User not logged in', response.json['error'])

    def test_get_user_profile_logged_in(self):
        with self.app.test_request_context():
            session['user_id'] = 1
            user = users[0]
            response = self.client.get('/api/user/profile')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, user.__dict__)

    def test_get_user_profile_not_found(self):
        with self.app.test_request_context():
            session['user_id'] = 999
            response = self.client.get('/api/user/profile')
            self.assertEqual(response.status_code, 404)
            self.assertIn('User not found', response.json['error'])

    def test_get_user_courses_not_logged_in(self):
        with self.app.test_request_context():
            session['user_id'] = None
            response = self.client.get('/api/user/courses')
            self.assertEqual(response.status_code, 401)
            self.assertIn('User not logged in', response.json['error'])

    def test_get_user_courses_logged_in(self):
        with self.app.test_request_context():
            session['user_id'] = 1
            user_courses = [course.__dict__ for course in courses if course.id in users[0].courses]
            response = self.client.get('/api/user/courses')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, user_courses)

    def test_get_user_courses_user_not_found(self):
        with self.app.test_request_context():
            session['user_id'] = 999
            response = self.client.get('/api/user/courses')
            self.assertEqual(response.status_code, 404)
            self.assertIn('User not found', response.json['error'])

    def test_get_courses(self):
        response = self.client.get('/api/courses')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), len(courses))

    def test_get_course_details(self):
        course_id = 1
        course = courses[0]
        response = self.client.get(f'/api/course/{course_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, course.__dict__)

    def test_get_course_details_not_found(self):
        response = self.client.get('/api/course/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Course not found', response.json['error'])

    def test_login_success(self):
        with patch('app.routes.otps', {'pia@example.com': 123456}):
            data = {'email': 'pia@example.com', 'otp': 123456}
            response = self.client.post('/api/login', json=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Logged in successfully')

    def test_login_invalid_otp(self):
        with patch('app.routes.otps', {'john.doe@example.com': 123456}):
            data = {'email': 'john.doe@example.com', 'otp': 654321}
            response = self.client.post('/api/login', json=data)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.json['success'])
            self.assertEqual(response.json['message'], 'Invalid OTP or user not found')

    def test_login_user_not_found(self):
        with patch('app.routes.otps', {'notfound@example.com': 123456}):
            data = {'email': 'notfound@example.com', 'otp': 123456}
            response = self.client.post('/api/login', json=data)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.json['success'])
            self.assertEqual(response.json['message'], 'Invalid OTP or user not found')

    def test_logout(self):
        with self.app.test_request_context():
            session['user_id'] = 1
            response = self.client.post('/api/logout')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json['success'])
            self.assertEqual(response.json['message'], 'Logged out successfully')


    def test_generate_otp_success(self):
        data = {'email': 'rey@example.com'}
        response = self.client.post('/api/user/generate-otp', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['message'], 'OTP sent successfully')

    def test_generate_otp_email_not_found(self):
        data = {'email': 'notfound@example.com'}
        response = self.client.post('/api/user/generate-otp', json=data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json['success'])
        self.assertEqual(response.json['message'], 'Email not found')

    def test_generate_otp_internal_error(self):
            data = {'email': 'yac@example.com'}
            response = self.client.post('/api/user/generate-otp', json=data)
            self.assertEqual(response.status_code, 404)
            self.assertFalse(response.json['success'])
            self.assertEqual(response.json['message'], 'Email not found')

    def test_enroll_success(self):
        with self.app.test_request_context():
            session['user_id'] = 1
            data = {'courseId': 1}
            response = self.client.post('/api/enroll', json=data)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json['success'])
            self.assertEqual(response.json['message'], 'Enrolled successfully')

    def test_enroll_not_logged_in(self):
        session['user_id'] = None
        data = {'courseId': 1}
        response = self.client.post('/api/enroll', json=data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('User not logged in', response.json['error'])

    def test_enroll_user_not_found(self):
        with self.app.test_request_context():
            session['user_id'] = 999
            data = {'courseId': 1}
            response = self.client.post('/api/enroll', json=data)
            self.assertEqual(response.status_code, 500)
            self.assertIn('Internal server error', response.json['error'])

    def test_get_user_profile_session_clear(self):
        with self.app.test_request_context():
            session.clear()
            response = self.client.get('/api/user/profile')
            self.assertEqual(response.status_code, 401)
            self.assertIn('User not logged in', response.json['error'])

    def test_get_user_courses_session_clear(self):
        with self.app.test_request_context():
            session.clear()
            response = self.client.get('/api/user/courses')
            self.assertEqual(response.status_code, 401)
            self.assertIn('User not logged in', response.json['error'])

    def test_login_missing_data(self):
        data = {'email': 'john.doe@example.com'}
        response = self.client.post('/api/login', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json['success'])
        self.assertIn('Invalid OTP or user not found', response.json['message'])

    def test_generate_otp_missing_email(self):
        data = {}
        response = self.client.post('/api/user/generate-otp', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json['success'])
        self.assertIn('Email is required', response.json['message'])

    def test_generate_otp_email_exception(self):
        with patch('app.routes.otps', {'john.doe@example.com': 123456}):
            data = {'email': 'john.doe@example.com'}
            with self.app.test_request_context():
                response = self.client.post('/api/user/generate-otp', json=data)
                self.assertEqual(response.status_code, 404)
                self.assertFalse(response.json['success'])

    def test_get_course_details_invalid_id(self):
        """Test retrieving course details with invalid ID."""
        response = self.client.get('/api/course/abc')
        self.assertEqual(response.status_code, 404)


    def test_register_user_existing_email(self):
        """Test registering a user with an existing email."""
        existing_email = users[0].email
        data = {'name': 'Duplicate User', 'email': existing_email}
        response = self.client.post('/api/user/register', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['message'], 'Email already exists')



    def test_enroll_missing_course_id(self):
        """Test enrolling in a course with missing course ID."""
        with self.app.test_request_context():
            session['user_id'] = 1
            data = {}
            response = self.client.post('/api/enroll', json=data)
            self.assertEqual(response.status_code, 400)
            self.assertIn('courseId is required', response.json['error'])

    def test_enroll_invalid_course_id(self):
        """Test enrolling in a course with invalid course ID."""
        with self.app.test_request_context():
            session['user_id'] = 1
            data = {'courseId': 'invalid'}
            response = self.client.post('/api/enroll', json=data)
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid course ID', response.json['error'])

    def test_enroll_course_not_found(self):
        """Test enrolling in a course that does not exist."""
        with self.app.test_request_context():
            session['user_id'] = 1
            data = {'courseId': 999}
            response = self.client.post('/api/enroll', json=data)
            #self.assertEqual(response.status_code, 404)
            self.assertIn('course not found', response.json['error'])

    def test_send_email_success(self):
        """Test sending an email successfully."""
        with patch('smtplib.SMTP') as mock_smtp:
            mock_instance = mock_smtp.return_value
            mock_instance.sendmail.return_value = {}
            success = send_email('test@example.com', 123456)
            self.assertTrue(success)

    def test_get_user_profile_no_credentials(self):
        """Test retrieving user profile with no credentials."""
        with self.app.test_request_context():
            session.clear()
            response = self.client.get('/api/user/profile')
            self.assertEqual(response.status_code, 401)
            self.assertIn('User not logged in', response.json['error'])

    def test_get_user_courses_no_credentials(self):
        """Test retrieving user courses with no credentials."""
        with self.app.test_request_context():
            session.clear()
            response = self.client.get('/api/user/courses')
            self.assertEqual(response.status_code, 401)
            self.assertIn('User not logged in', response.json['error'])

    def test_user_register_duplicate_email(self):
        """Test registering a user with a duplicate email."""
        existing_email = users[0].email
        data = {'name': 'New User', 'email': existing_email}
        response = self.client.post('/api/user/register', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.json['success'])
        self.assertEqual(response.json['message'], 'Email already exists')

    def test_generate_otp_with_invalid_email(self):
        """Test generating OTP with invalid email."""
        data = {'email': 'invalid-email'}
        response = self.client.post('/api/user/generate-otp', json=data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json['success'])
        self.assertEqual(response.json['message'], 'Email not found')

if __name__ == '__main__':
    unittest.main()
