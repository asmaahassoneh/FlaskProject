# Flask Student Portal v1

A mini Flask project for student registration and management using **Flask**, **Blueprints**, **Jinja2 templates**, and **basic route testing**.

## Features

- Home page with navigation
- Register a student using a form
- Validate form input before saving
- Store students in an in-memory list
- Prevent duplicate student IDs
- View all students
- View details of a single student
- Custom 404 page for missing students/pages
- Basic unit tests using Flask test client

## Tech Stack

- Python
- Flask
- Jinja2
- Pytest

## Project Structure

```text
flask-student-portal-v1/
│
├── app.py
├── routes/
│   ├── __init__.py
│   └── student_routes.py
├── data/
│   ├── __init__.py
│   └── store.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── register.html
│   ├── students.html
│   ├── student_details.html
│   └── 404.html
├── static/
│   └── style.css
├── tests/
│   └── test_routes.py
├── README.md
└── requirements.txt
```

---

# Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

Run the main program:

```bash
python app.py
```

Then open:

```
http://127.0.0.1:5000
```

---

Run linting and formatting:

```bash
flake8 .
black .
```

## 🧪 Running Tests

```bash
python -m pytest
```
