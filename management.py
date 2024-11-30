import pickle
import random

class Student:
    def __init__(self, name, batch, department, courses=None):
        self.name = name
        self.batch = batch
        self.department = department
        self.courses = list(set(courses)) if courses else []  # Ensure unique courses

    def add_courses(self, courses):
        self.courses = list(set(self.courses + courses))
    
    def remove_courses(self, courses):
        self.courses = list(set(self.courses).difference(courses))
    
    def __str__(self):
        course_names = [course.name for course in self.courses]
        return f"{self.name} ({self.batch}) - {self.department} - {', '.join(course_names)}"
    
class Course:
    def __init__(self, name, code, department, core_for=None):
        self.name = name
        self.code = code
        self.department = department
        self.core_for = core_for      # core_for = (batch, department)

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.department}"
    
    def __eq__(self, other):
        return self.code == other.code

    def __hash__(self):
        return hash(self.code)
    
class Management:
    def __init__(self, students=None, courses=None):
        self.students = list(set(students)) if students else []
        self.courses = list(set(courses)) if courses else []

    def add_students(self, students):
        self.students = list(set(self.students + students))

    def add_courses(self, courses):
        self.courses = list(set(self.courses + courses))

    def remove_students(self, students):
        self.students = list(set(self.students).difference(students))

    def remove_courses(self, courses):
        self.courses = list(set(self.courses).difference(courses))

    def get_students(self, department=None):
        if department:
            return [student for student in self.students if student.department == department]
        return self.students

    def get_courses(self, department=None):
        if department:
            return [course for course in self.courses if course.department == department]
        return self.courses

    def get_students_for_course(self, course_name):
        return [student for student in self.students if any(course.name == course_name for course in student.courses)]

    def get_courses_for_student(self, student):
        return [course for course in self.courses if course in student.courses]

    def get_core_courses(self, batch, department):
        if batch and department:
            return [course for course in self.courses if course.core_for == (batch, department)]
        elif batch and not department:
            return [course for course in self.courses if course.core_for and course.core_for[0] == batch]
        elif department and not batch:
            return [course for course in self.courses if course.core_for and course.core_for[1] == department]
        else:
            return [course for course in self.courses if course.core_for]
        
    def list_courses_with_student_count(self):
        course_student_count = {course: 0 for course in self.courses}
        
        for student in self.students:
            for course in student.courses:
                if course in course_student_count:
                    course_student_count[course] += 1

        sorted_courses = sorted(self.courses, key=lambda c: (c.department, c.core_for if c.core_for else ()))

        for course in sorted_courses:
            core_for_str = f" (Core for batch {course.core_for[0]})" if course.core_for else ""
            print(f"{course.name} ({course.code}) - {course.department}{core_for_str}: {course_student_count[course]} students")

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)

    def __str__(self):
        return f"Management System with {len(self.students)} students and {len(self.courses)} courses"
    
def generate_random_data(p=0.5):
    departments = ["SMS", "SPS", "SBS", "SCS", "SCoS", "SEPS", "SHSS"]
    batches = [2020, 2021, 2022, 2023, 2024]
    num_students = random.randint(1000, 1200)
    num_courses = random.randint(70, 80)

    # Generate courses
    courses = []
    for i in range(num_courses):
        department = random.choice(departments)
        student_departments = ["SMS", "SPS", "SBS", "SCS"]
        batch = random.choice(batches) if department not in ["SEPS", "SHSS", "SCoS"] else 2024
        core_for = (batch, department) if department not in ["SEPS"] and random.random() < p else None
        course = Course(f"Course {i+1}", f"CODE{i+1}", department, core_for)
        courses.append(course)

    # Generate students
    students = []
    for i in range(num_students):
        name = f"Student {i+1}"
        batch = random.choice(batches)
        department = random.choice(student_departments)
        student_courses = [course for course in courses if course.core_for == (batch, department)]
        num_additional_courses = random.randint(0, max(0, 5 - len(student_courses)))
        additional_courses = random.sample([course for course in courses if course not in student_courses], num_additional_courses)
        student_courses.extend(additional_courses)
        student = Student(name, batch, department, student_courses)
        students.append(student)

    return students, courses


# Example usage
if __name__ == "__main__":
    students, courses = generate_random_data(p=0.5)

    management = Management()
    management.add_students(students)
    management.add_courses(courses)

    # Save to file
    management.save_to_file('management_data.pkl')

    # Load from file
    loaded_management = Management.load_from_file('management_data.pkl')
    print(loaded_management)

    # Print details of loaded students and courses
    for student in loaded_management.get_students():
        print(student)

    for course in loaded_management.get_courses():
        print(course)

    # List courses with student count
    loaded_management.list_courses_with_student_count()