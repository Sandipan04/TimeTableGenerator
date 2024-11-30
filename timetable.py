from management import Management, Student, Course

class TimeTable:
    def __init__(self, management, num_slots=6):
        self.management = management
        self.courses = management.get_courses()
        self.students = management.get_students()
        self.num_slots = num_slots
        self.slots = [[] for _ in range(num_slots)]  # List of lists to store courses in each slot
        self.course_index = {course: idx for idx, course in enumerate(self.courses)}
        self.index_course = {idx: course for course, idx in self.course_index.items()}
        self.common_students_matrix = self.create_common_students_matrix()
        self.normalized_matrix = self.normalize_common_students_matrix()

    def create_common_students_matrix(self):
        num_courses = len(self.courses)
        matrix = [[0] * num_courses for _ in range(num_courses)]

        for student in self.students:
            for i in range(len(student.courses)):
                for j in range(i + 1, len(student.courses)):
                    course1 = student.courses[i]
                    course2 = student.courses[j]
                    idx1 = self.course_index[course1]
                    idx2 = self.course_index[course2]
                    matrix[idx1][idx2] += 1
                    matrix[idx2][idx1] += 1  # Since the matrix is symmetric

        return matrix

    def normalize_common_students_matrix(self):
        num_courses = len(self.courses)
        normalized_matrix = [[0] * num_courses for _ in range(num_courses)]

        for i in range(num_courses):
            for j in range(num_courses):
                if i != j:
                    total_students = len([student for student in self.students if self.courses[i] in student.courses or self.courses[j] in student.courses])
                    if total_students > 0:
                        normalized_matrix[i][j] = self.common_students_matrix[i][j] / total_students

        return normalized_matrix

    def assign_slot(self, course, slot_number):
        if course in self.courses and 0 <= slot_number < len(self.slots):
            self.slots[slot_number].append(course)

    def remove_slot(self, course):
        for slot_courses in self.slots:
            if course in slot_courses:
                slot_courses.remove(course)

    def empty_all_slots(self):
        self.slots = [[] for _ in range(self.num_slots)]

    def check_clashes(self):
        clashes = 0
        for slot_courses in self.slots:
            for i in range(len(slot_courses)):
                for j in range(i + 1, len(slot_courses)):
                    course1 = slot_courses[i]
                    course2 = slot_courses[j]
                    idx1 = self.course_index[course1]
                    idx2 = self.course_index[course2]
                    clashes += self.common_students_matrix[idx1][idx2]
        return clashes

    def print_common_students_matrix(self):
        print("Common Students Matrix:")
        header = " " * 10 + " ".join(f"{course.code:^10}" for course in self.courses)
        print(header)
        for i, course1 in enumerate(self.courses):
            row = f"{course1.code:10}" + " ".join(f"{self.common_students_matrix[i][j]:^10}" for j in range(len(self.courses)))
            print(row)

    def __str__(self):
        result = "TimeTable:\n"
        for i, slot_courses in enumerate(self.slots):
            result += f"Slot {i+1}: " + ", ".join(course.name for course in slot_courses) + "\n"
        return result

    def greedy_slot_allocation(self):
        num_courses = len(self.courses)
        courses_per_slot = num_courses // self.num_slots
        extra_courses = num_courses % self.num_slots

        # Step 1: Find the pair of courses with the maximum number of common students
        max_common_students = 0
        course_a, course_b = None, None
        for i in range(num_courses):
            for j in range(i + 1, num_courses):
                if self.common_students_matrix[i][j] > max_common_students:
                    max_common_students = self.common_students_matrix[i][j]
                    course_a, course_b = self.courses[i], self.courses[j]

        # Assign course_a to slot 0 and course_b to slot 1
        self.assign_slot(course_a, 0)
        self.assign_slot(course_b, 1)

        # Step 2: Iteratively assign courses to slots
        assigned_courses = {course_a, course_b}
        for i in range(2, num_courses):
            slot = i % self.num_slots
            best_value = 1
            best_course = None
            for course in self.courses:
                if course not in assigned_courses:
                    value = 1
                    idx1 = self.course_index[course]
                    for assigned_course in assigned_courses:
                        idx2 = self.course_index[assigned_course]
                        if assigned_course in self.slots[slot]:
                            value *= self.normalized_matrix[idx1][idx2]
                        else:
                            value *= (1 - self.normalized_matrix[idx1][idx2])
                    if value < best_value:
                        best_value = value
                        best_course = course
            self.assign_slot(best_course, slot)
            assigned_courses.add(best_course)

# Example usage
if __name__ == "__main__":
    # Assuming `students` is a list of Student objects and `courses` is a list of Course objects
    loaded_management = Management.load_from_file('management_data.pkl')
    print(loaded_management)

    timetable = TimeTable(loaded_management)
    # timetable.print_common_students_matrix()

    # Perform greedy slot allocation
    timetable.greedy_slot_allocation()

    # Print the timetable
    print(timetable)

    # Check the number of clashes
    clashes = timetable.check_clashes()
    print(f"Number of clashes: {clashes}")