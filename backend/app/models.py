class User:
    def __init__(self, id, name, email, courses):
        self.id = id
        self.name = name
        self.email = email
        self.courses = courses

class Course:
    def __init__(self, id, title, description, instructor, duration):
        self.id = id
        self.title = title
        self.description = description
        self.instructor = instructor
        self.duration = duration

class Enrollment:
    def __init__(self, id, user_id, course_id):
        self.id = id
        self.user_id = user_id
        self.course_id = course_id
