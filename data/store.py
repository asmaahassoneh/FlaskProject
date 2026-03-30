students = []


def get_all_students():
    """Return all students."""
    return list(students)


def get_student_by_id(student_id):
    """Return a student by ID or None if not found."""
    normalized_id = student_id.strip().upper()

    for student in students:
        if student["student_id"] == normalized_id:
            return student
    return None


def student_id_exists(student_id):
    """Check whether a student ID already exists."""
    return get_student_by_id(student_id) is not None


def add_student(student):
    """Add a new student"""
    students.append(student)


def clear_students():
    """Clear all students. Useful for testing."""
    students.clear()
