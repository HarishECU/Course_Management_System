from flask import Blueprint, jsonify, request
from flask_cors import CORS
from .models import User, Course, Enrollment
import json
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

main_blueprint = Blueprint('main', __name__)
CORS(main_blueprint, supports_credentials=True)

# Load Data
with open('data/users.json') as f:
    users_data = json.load(f)
users = [User(**user) for user in users_data]

with open('data/courses.json') as f:
    courses_data = json.load(f)
courses = [Course(**course) for course in courses_data]

with open('data/enrollments.json') as f:
    enrollments_data = json.load(f)
enrollments = [Enrollment(**enrollment) for enrollment in enrollments_data]

# In-memory storage for OTPs
otps = {}
session = {'user_id': None}  # Custom session dictionary

@main_blueprint.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({"error": "User not logged in"}), 401
    
    user = next((user for user in users if user.id == user_id), None)
    if user:
        return jsonify(user.__dict__)
    return jsonify({"error": "User not found"}), 404

@main_blueprint.route('/api/user/courses', methods=['GET'])
def get_user_courses():
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({"error": "User not logged in"}), 401
    
    user = next((user for user in users if user.id == user_id), None)
    if user:
        user_courses = [course.__dict__ for course in courses if course.id in user.courses]
        return jsonify(user_courses)
    return jsonify({"error": "User not found"}), 404

@main_blueprint.route('/api/courses', methods=['GET'])
def get_courses():
    courses_list = [course.__dict__ for course in courses]
    return jsonify(courses_list)

@main_blueprint.route('/api/course/<int:id>', methods=['GET'])
def get_course_details(id):
    course = next((course for course in courses if course.id == id), None)
    if course:
        return jsonify(course.__dict__)
    return jsonify({"error": "Course not found"}), 404

@main_blueprint.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        otp = data.get('otp')

        user = next((user for user in users if user.email == email), None)
        if user and otps.get(email) == int(otp):
            session['user_id'] = user.id  # Set the authenticated user's ID
            return jsonify({"success": True, "message": "Logged in successfully", "user": user.__dict__})
        else:
            return jsonify({"success": False, "message": "Invalid OTP or user not found"})
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@main_blueprint.route('/api/logout', methods=['POST'])
def logout():
    session['user_id'] = None
    return jsonify({"success": True, "message": "Logged out successfully"})

@main_blueprint.route('/api/user/register', methods=['POST'])
def register():
    try:
        data = request.json
        new_id = len(users) + 1
        new_user = User(
            id=new_id,
            name=data.get('name'),
            email=data.get('email'),
            courses=[]
        )
        
        if data.get('name') == "" and data.get('email') == "":
            return jsonify({"success": False,"message": "All fields are required"}), 201
        if data.get('name') == "":
            return jsonify({"success": False,"message": "Name is required"}), 201
        if data.get('email') == "":
            return jsonify({"success": False,"message": "Email is required"}), 201
        email=data.get('email')
        user = next((user for user in users if user.email == email), None)
        if user:
            return jsonify({"success": False,"message": "Email already exists"}), 201
        else:
            users.append(new_user)
        
        # Optionally save the updated users list to the JSON file
        with open('data/users.json', 'w') as f:
            json.dump([user.__dict__ for user in users], f, indent=4)
        return jsonify({"success": True, "message": "User registered successfully", "user": new_user.__dict__}), 201
    except Exception as e:
        print(f"Error during registration: {e}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@main_blueprint.route('/api/user/generate-otp', methods=['POST'])
def generate_otp():
    try:
        data = request.json
        email = data.get('email')
        if not email:
            return jsonify({"success": False, "message": "Email is required"}), 400

        # Check if email exists in users
        if email not in [user.email for user in users]:
            return jsonify({"success": False, "message": "Email not found"}), 404
        
        # Generate OTP
        otp = random.randint(100000, 999999)
        otps[email] = otp

        # Send OTP via email (dummy implementation)
        if not send_email(email, otp):
            return jsonify({"success": False, "message": "Failed to send OTP"}), 500

        return jsonify({"success": True, "message": "OTP sent successfully","otp":otp})
    except Exception as e:
        print(f"Error generating OTP: {e}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

def send_email(email, otp):
    try:
        # Dummy email sending function
        sender_email = "schooll.m.s2024@gmail.com"
        sender_password = "LMSschool"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = "Your OTP Code"

        body = f"Your OTP code is {otp}"
        msg.attach(MIMEText(body, 'plain'))

        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.starttls()
        # server.login(sender_email, sender_password)
        # text = msg.as_string()
        # server.sendmail(sender_email, email, text)
        # server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@main_blueprint.route('/api/enroll', methods=['POST'])
def enroll():
    data = request.json
    user_id = session.get('user_id')
    
    course_id = data.get('courseId')
    if course_id is None:
        return jsonify({"error": "courseId is required"}), 400
    if type(course_id) != int:
        return jsonify({"error": "Invalid course ID"}), 400
    course_found = next((course for course in courses if course.id == course_id),None)
    if course_found is None:
        return jsonify({"error": "course not found"}), 404

    if user_id == None:
        return jsonify({"error": "User not logged in"}), 401
    
    
    enrollment = Enrollment(id=len(enrollments) + 1, user_id=user_id, course_id=course_id)
    enrollments.append(enrollment)

    user = next((user for user in users if user.id == user_id), None)
    if user:
        user.courses.append(course_id)
    else:
        return jsonify({"error": "Internal server error"}), 500

    # Save the updated enrollments and users to the JSON files
    with open('data/enrollments.json', 'w') as f:
        json.dump([enrollment.__dict__ for enrollment in enrollments], f, indent=4)
    with open('data/users.json', 'w') as f:
        json.dump([user.__dict__ for user in users], f, indent=4)
    
    return jsonify({"success": True, "message": "Enrolled successfully"})
