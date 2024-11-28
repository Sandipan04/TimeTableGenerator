# TimeTableGenerator

## Overview
The TimeTableGenerator project is an attempt to design an algorithm for generating timetables for schools, colleges, and institutes. The goal is to address clashes between courses, considering students common to multiple courses and the limited number of slots available for courses each day of the week. We are currently in the process of building the necessary database tools to support this algorithm.

## Features
- **Student and Course Management**: Add and remove students and courses.
- **Random Data Generation**: Generate a random database of students and courses with specific conditions.
- **Data Persistence**: Save and load the database to/from a file using serialization.
- **Course Listing**: List all courses with the number of students enrolled, sorted by department and core course batch.

## Classes and Methods

### Student Class
Represents a student with attributes:
- `name`: The name of the student.
- `batch`: The batch year of the student.
- `department`: The department of the student.
- `courses`: A list of courses the student is enrolled in.

### Course Class
Represents a course with attributes:
- `name`: The name of the course.
- `code`: The code of the course.
- `department`: The department offering the course.
- `core_for`: A tuple indicating the batch and department for which the course is a core course.

### Management Class
Manages the database of students and courses with methods:
- `add_student(students)`: Add a list of students.
- `add_course(courses)`: Add a list of courses.
- `remove_student(students)`: Remove a list of students.
- `remove_course(courses)`: Remove a list of courses.
- `get_students(department=None)`: Get a list of students, optionally filtered by department.
- `get_courses(department=None)`: Get a list of courses, optionally filtered by department.
- `get_students_for_course(course_name)`: Get a list of students enrolled in a specific course.
- `get_courses_for_student(student)`: Get a list of courses a specific student is enrolled in.
- `get_core_courses(batch, department)`: Get a list of core courses for a specific batch and department.
- `save_to_file(filename)`: Save the database to a file.
- `load_from_file(filename)`: Load the database from a file.
- `list_courses_with_student_count()`: List all courses with the number of students enrolled, sorted by department and core course batch.

### Random Data Generation
The `generate_random_data(p=0.5)` function generates a random database of students and courses with the following conditions:
- Departments: SMS, SPS, SBS, SCS, SCoS, SEPS, SHSS.
- Batches: 2020, 2021, 2022, 2023, 2024.
- No core courses in SEPS department.
- Core courses in SHSS and SCoS only for batch 2024.
- Courses can be core courses with a probability `p`.
- Students must take all core courses for their batch and department.
- A student cannot have more than 5 courses in total.

## Example Usage
```python
# Generate random data
students, courses = generate_random_data(p=0.5)

# Create a management instance
management = Management()
management.add_student(students)
management.add_course(courses)

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
loaded_management.list_courses_with_student_count()```