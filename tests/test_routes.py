import pytest

from app import create_app
from data.store import clear_students, students


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    clear_students()
    yield
    clear_students()


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to Flask Student Portal v1" in response.data


def test_register_page_get(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Register Student" in response.data


def test_register_student_success(client):
    response = client.post(
        "/register",
        data={
            "name": "Asmaa",
            "student_id": "123",
            "gpa": "3.8",
            "major": "Computer Engineering",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"All Students" in response.data
    assert len(students) == 1
    assert students[0]["name"] == "Asmaa"
    assert students[0]["student_id"] == "123"
    assert students[0]["gpa"] == 3.8
    assert students[0]["major"] == "Computer Engineering"


def test_register_student_missing_fields(client):
    response = client.post(
        "/register",
        data={
            "name": "",
            "student_id": "123",
            "gpa": "3.5",
            "major": "IT",
        },
    )

    assert response.status_code == 200
    assert b"All fields are required." in response.data
    assert len(students) == 0


def test_register_student_duplicate_id(client):
    students.append(
        {
            "name": "Ali",
            "student_id": "100",
            "gpa": 3.2,
            "major": "CS",
        }
    )

    response = client.post(
        "/register",
        data={
            "name": "Sara",
            "student_id": "100",
            "gpa": "3.7",
            "major": "Math",
        },
    )

    assert response.status_code == 200
    assert b"Student ID already exists." in response.data
    assert len(students) == 1


def test_register_student_invalid_gpa_text(client):
    response = client.post(
        "/register",
        data={
            "name": "Ali",
            "student_id": "200",
            "gpa": "abc",
            "major": "IT",
        },
    )

    assert response.status_code == 200
    assert b"GPA must be a valid number." in response.data
    assert len(students) == 0


def test_register_student_gpa_below_range(client):
    response = client.post(
        "/register",
        data={
            "name": "Lina",
            "student_id": "201",
            "gpa": "-1",
            "major": "Math",
        },
    )

    assert response.status_code == 200
    assert b"GPA must be between 0 and 4." in response.data
    assert len(students) == 0


def test_register_student_gpa_above_range(client):
    response = client.post(
        "/register",
        data={
            "name": "Omar",
            "student_id": "202",
            "gpa": "4.5",
            "major": "Physics",
        },
    )

    assert response.status_code == 200
    assert b"GPA must be between 0 and 4." in response.data
    assert len(students) == 0


def test_register_student_gpa_zero(client):
    response = client.post(
        "/register",
        data={
            "name": "Noor",
            "student_id": "300",
            "gpa": "0",
            "major": "Biology",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert len(students) == 1
    assert students[0]["gpa"] == 0.0


def test_register_student_gpa_four(client):
    response = client.post(
        "/register",
        data={
            "name": "Yousef",
            "student_id": "301",
            "gpa": "4",
            "major": "Medicine",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert len(students) == 1
    assert students[0]["gpa"] == 4.0


def test_register_student_strips_spaces(client):
    response = client.post(
        "/register",
        data={
            "name": "  Asmaa  ",
            "student_id": "  abc123  ",
            "gpa": "3.5",
            "major": "  Computer Engineering  ",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert len(students) == 1
    assert students[0]["name"] == "Asmaa"
    assert students[0]["student_id"] == "ABC123"
    assert students[0]["major"] == "Computer Engineering"


def test_list_students_page_empty(client):
    response = client.get("/students")
    assert response.status_code == 200
    assert b"No students registered yet." in response.data


def test_list_students_page_with_students(client):
    students.append(
        {
            "name": "Ali",
            "student_id": "111",
            "gpa": 3.4,
            "major": "CS",
        }
    )

    response = client.get("/students")
    assert response.status_code == 200
    assert b"Ali" in response.data
    assert b"111" in response.data
    assert b"CS" in response.data


def test_student_details_success(client):
    students.append(
        {
            "name": "Sara",
            "student_id": "222",
            "gpa": 3.9,
            "major": "Engineering",
        }
    )

    response = client.get("/students/222")
    assert response.status_code == 200
    assert b"Student Details" in response.data
    assert b"Sara" in response.data
    assert b"222" in response.data
    assert b"Engineering" in response.data


def test_student_details_not_found(client):
    response = client.get("/students/999")
    assert response.status_code == 404
    assert b"404 - Page Not Found" in response.data


def test_register_redirects_after_success(client):
    response = client.post(
        "/register",
        data={
            "name": "Maha",
            "student_id": "555",
            "gpa": "3.6",
            "major": "IT",
        },
    )

    assert response.status_code == 302
    assert "/students" in response.headers["Location"]


def test_duplicate_student_id_case_insensitive(client):
    students.append(
        {
            "name": "Ali",
            "student_id": "ABC1",
            "gpa": 3.0,
            "major": "CS",
        }
    )

    response = client.post(
        "/register",
        data={
            "name": "Omar",
            "student_id": "abc1",
            "gpa": "3.2",
            "major": "Math",
        },
    )

    assert response.status_code == 200
    assert b"Student ID already exists." in response.data
    assert len(students) == 1
