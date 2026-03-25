from flask import Blueprint, abort, redirect, render_template, request, url_for

from data.store import (
    add_student,
    get_all_students,
    get_student_by_id,
    student_id_exists,
)

student_bp = Blueprint("student_bp", __name__)

REQUIRED_FIELDS_ERROR = "All fields are required."
DUPLICATE_ID_ERROR = "Student ID already exists."
INVALID_GPA_ERROR = "GPA must be a valid number."
GPA_RANGE_ERROR = "GPA must be between 0 and 4."


def normalize_text(value):
    return value.strip()


def normalize_student_id(student_id):
    return student_id.strip().upper()


def validate_student_form(name, student_id, gpa_raw, major):
    if not name or not student_id or not gpa_raw or not major:
        return REQUIRED_FIELDS_ERROR, None

    try:
        gpa = round(float(gpa_raw), 2)
    except ValueError:
        return INVALID_GPA_ERROR, None

    if not 0 <= gpa <= 4:
        return GPA_RANGE_ERROR, None

    if student_id_exists(student_id):
        return DUPLICATE_ID_ERROR, None

    return None, gpa


@student_bp.route("/")
def home():
    return render_template("home.html")


@student_bp.route("/register", methods=["GET", "POST"])
def register_student():
    form_data = {
        "name": "",
        "student_id": "",
        "gpa": "",
        "major": "",
    }

    if request.method == "GET":
        return render_template("register.html", error=None, form_data=form_data)

    name = normalize_text(request.form.get("name", ""))
    student_id = normalize_student_id(request.form.get("student_id", ""))
    gpa_raw = normalize_text(request.form.get("gpa", ""))
    major = normalize_text(request.form.get("major", ""))

    form_data = {
        "name": name,
        "student_id": student_id,
        "gpa": gpa_raw,
        "major": major,
    }

    error, gpa = validate_student_form(name, student_id, gpa_raw, major)

    if error:
        return render_template("register.html", error=error, form_data=form_data)

    student = {
        "name": name,
        "student_id": student_id,
        "gpa": gpa,
        "major": major,
    }

    add_student(student)
    return redirect(url_for("student_bp.list_students"))


@student_bp.route("/students")
def list_students():
    students = get_all_students()
    return render_template("students.html", students=students)


@student_bp.route("/students/<student_id>")
def student_details(student_id):
    student = get_student_by_id(student_id)

    if student is None:
        abort(404)

    return render_template("student_details.html", student=student)
