import sqlite3
from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from hrapp.models import Employee, Department, TrainingProgram
from ..connection import Connection


def create_employee(cursor, row):
    _row = sqlite3.Row(cursor, row)

    e = Employee()
    e.id = _row["id"]
    e.first_name = _row["first_name"]
    e.last_name = _row["last_name"]

    e.training_programs = []

    t = TrainingProgram()
    t.title = _row["training_program"]

    d = Department()
    d.name = _row["department"]

    c = Computer()
    c.make = _row["computer"]

    e.department = d
    e.computer = c

    return (e, )


def get_employee(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_employee

        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.id,
            e.first_name,
            e.last_name,
            e.start_date,
            e.is_supervisor,
            d.name department,
            c.make computer
        FROM
            hrapp_employee e
            JOIN hrapp_department d ON e.department_id = d.id 
            LEFT JOIN hrapp_employeecomputer ec ON e.id = ec.employee_id
            LEFT JOIN hrapp_computer c ON c.id = ec.id
        WHERE e.id = ?
        """, (employee_id,))

        return db_cursor.fetchone()


# @login_required
def library_details(request, library_id):
    if request.method == 'GET':
        library = get_library(library_id)

        template = 'libraries/detail.html'
        context = {
            'library': library
        }

        return render(request, template, context)
