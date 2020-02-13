import sqlite3
from django.shortcuts import render
from hrapp.models import Employee, Department, Computer, TrainingProgram
from ..connection import Connection


def create_employee(cursor, row):
    _row = sqlite3.Row(cursor, row)

    e = Employee()
    e.id = _row["id"]
    e.first_name = _row["first_name"]
    e.last_name = _row["last_name"]

    d = Department()
    d.name = _row["department"]

    c = Computer()
    c.make = _row["computer"]

    e.department = d
    e.computer = c

    return e


def create_training_program(cursor, row):
    _row = sqlite3.Row(cursor, row)

    t = TrainingProgram()
    t.title = _row["title"]

    return t


def get_employee(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_employee
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.first_name,
            e.last_name,
            d.name department,
            c.make computer
        FROM
            hrapp_employee e
            JOIN hrapp_department d ON e.department_id = d.id
            LEFT JOIN hrapp_employeecomputer ec ON e.id = ec.employee_id
            LEFT JOIN hrapp_computer c ON c.id = ec.computer_id
        WHERE e.id = ?
        """, (employee_id,))

        return db_cursor.fetchone()


def get_employee_training(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_training_program

        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.id,
            t.title
        FROM
            hrapp_employee e
            LEFT JOIN hrapp_trainingprogramemployee te ON e.id = te.employee_id
            LEFT JOIN hrapp_trainingprogram t ON t.id = te.training_program_id
        WHERE
            e.id = ?
        """, (employee_id,))

        return db_cursor.fetchall()


def employee_details(request, employee_id):
    if request.method == 'GET':
        employee = get_employee(employee_id)
        curr_employee_training = get_employee_training(employee_id)

        template = 'employees/employee_detail.html'
        context = {
            'employee': employee,
            'training_programs': curr_employee_training
        }

        return render(request, template, context)
