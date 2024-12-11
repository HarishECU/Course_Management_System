import unittest
import sys
import os

# Add the parent directory of 'app' to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import User, Course, Enrollment

class TestModels(unittest.TestCase):

    # User Model Tests
    def test_user_model_creation(self):
        user = User(id=1, name="John Doe", email="john.doe@example.com", courses=[1, 2, 3])
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.courses, [1, 2, 3])

    def test_user_model_empty_courses(self):
        user = User(id=2, name="Jane Smith", email="jane.smith@example.com", courses=[])
        self.assertEqual(user.courses, [])

    def test_user_model_email_format(self):
        user = User(id=3, name="Alice Johnson", email="alice.johnson@example.com", courses=[4, 5])
        self.assertIn("@", user.email)
        self.assertIn(".", user.email)

    def test_user_model_id_type(self):
        user = User(id=4, name="Bob Brown", email="bob.brown@example.com", courses=[6])
        self.assertIsInstance(user.id, int)

    def test_user_model_name_type(self):
        user = User(id=5, name="Charlie Black", email="charlie.black@example.com", courses=[7, 8])
        self.assertIsInstance(user.name, str)

    def test_user_model_courses_type(self):
        user = User(id=6, name="David White", email="david.white@example.com", courses=[9])
        self.assertIsInstance(user.courses, list)

    def test_user_model_add_course(self):
        user = User(id=7, name="Eve Green", email="eve.green@example.com", courses=[])
        user.courses.append(10)
        self.assertIn(10, user.courses)

    def test_user_model_remove_course(self):
        user = User(id=8, name="Frank Blue", email="frank.blue@example.com", courses=[11, 12])
        user.courses.remove(12)
        self.assertNotIn(12, user.courses)

    def test_user_model_multiple_courses(self):
        user = User(id=9, name="Grace Red", email="grace.red@example.com", courses=[13, 14, 15])
        self.assertEqual(len(user.courses), 3)

    def test_user_model_no_courses(self):
        user = User(id=10, name="Henry Yellow", email="henry.yellow@example.com", courses=[])
        self.assertEqual(len(user.courses), 0)

    # Course Model Tests
    def test_course_model_creation(self):
        course = Course(id=1, title="Course 101", description="Introduction to Course 101", instructor="Jane Doe", duration="2 hours")
        self.assertEqual(course.id, 1)
        self.assertEqual(course.title, "Course 101")
        self.assertEqual(course.description, "Introduction to Course 101")
        self.assertEqual(course.instructor, "Jane Doe")
        self.assertEqual(course.duration, "2 hours")

    def test_course_model_title(self):
        course = Course(id=2, title="Course 202", description="Advanced Course 202", instructor="John Smith", duration="3 hours")
        self.assertIsInstance(course.title, str)

    def test_course_model_description(self):
        course = Course(id=3, title="Course 303", description="Mastering Course 303", instructor="Alice Brown", duration="4 hours")
        self.assertGreater(len(course.description), 0)

    def test_course_model_instructor(self):
        course = Course(id=4, title="Course 404", description="Expert Course 404", instructor="Bob White", duration="5 hours")
        self.assertIsInstance(course.instructor, str)

    def test_course_model_duration_format(self):
        course = Course(id=5, title="Course 505", description="Intro to Course 505", instructor="Charlie Green", duration="6 hours")
        self.assertTrue(course.duration.endswith("hours"))

    def test_course_model_multiple_courses(self):
        course1 = Course(id=6, title="Course 606", description="Course 606", instructor="David Black", duration="2 hours")
        course2 = Course(id=7, title="Course 707", description="Course 707", instructor="Eve Yellow", duration="3 hours")
        courses = [course1, course2]
        self.assertEqual(len(courses), 2)

    def test_course_model_same_instructor(self):
        course1 = Course(id=8, title="Course 808", description="Course 808", instructor="Frank Red", duration="4 hours")
        course2 = Course(id=9, title="Course 909", description="Course 909", instructor="Frank Red", duration="5 hours")
        self.assertEqual(course1.instructor, course2.instructor)

    def test_course_model_id_type(self):
        course = Course(id=10, title="Course 1010", description="Course 1010", instructor="Grace Blue", duration="6 hours")
        self.assertIsInstance(course.id, int)

    # Enrollment Model Tests
    def test_enrollment_model_creation(self):
        enrollment = Enrollment(id=1, user_id=1, course_id=1)
        self.assertEqual(enrollment.id, 1)
        self.assertEqual(enrollment.user_id, 1)
        self.assertEqual(enrollment.course_id, 1)

    def test_enrollment_model_user_id_type(self):
        enrollment = Enrollment(id=2, user_id=2, course_id=2)
        self.assertIsInstance(enrollment.user_id, int)

    def test_enrollment_model_course_id_type(self):
        enrollment = Enrollment(id=3, user_id=3, course_id=3)
        self.assertIsInstance(enrollment.course_id, int)

    def test_enrollment_model_id_type(self):
        enrollment = Enrollment(id=4, user_id=4, course_id=4)
        self.assertIsInstance(enrollment.id, int)

    def test_enrollment_model_multiple_enrollments(self):
        enrollment1 = Enrollment(id=5, user_id=5, course_id=5)
        enrollment2 = Enrollment(id=6, user_id=5, course_id=6)
        enrollments = [enrollment1, enrollment2]
        self.assertEqual(len(enrollments), 2)

if __name__ == '__main__':
    unittest.main()
