import sqlite3
from datetime import datetime
from django.urls import reverse
from django.shortcuts import render, redirect
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


def create_computer(cursor, row):
    _row = sqlite3.Row(cursor, row)

    c = Computer()
    c.make = _row["computer"]

    return c


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
            c.make computer,
            ec.assigned_date,
            ec.unassigned_date
        FROM
            hrapp_employee e
            JOIN hrapp_department d ON e.department_id = d.id
            LEFT JOIN hrapp_employeecomputer ec ON e.id = ec.employee_id
            LEFT JOIN hrapp_computer c ON c.id = ec.computer_id
        WHERE
            e.id = ?
        AND unassigned_date >= strftime('%Y-%m-%d','now') OR unassigned_date IS NULL
        AND assigned_date >= strftime('%Y-%m-%d','now')
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


def get_employee_computer(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_computer
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.first_name,
            e.last_name,
            d.name department,
            c.make computer,
            ec.assigned_date,
            ec.unassigned_date
        FROM
            hrapp_employee e
            JOIN hrapp_department d ON e.department_id = d.id
            LEFT JOIN hrapp_employeecomputer ec ON e.id = ec.employee_id
            LEFT JOIN hrapp_computer c ON c.id = ec.computer_id
        WHERE
            e.id = ?
        AND unassigned_date >= strftime('%Y-%m-%d','now') OR unassigned_date IS NULL
        AND assigned_date >= strftime('%Y-%m-%d','now')
        """, (employee_id,))

        return db_cursor.fetchone()


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

    elif request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                curr_employee_computer = get_employee_computer(employee_id)
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE hrapp_employee
                SET
                    last_name = ?,
                    department_id = ?
                WHERE id = ?;
                """,
                (
                    form_data['last_name'], form_data['department'], employee_id,
                ))

                # if an employee already has a computer & is being assigned to a new one, then they need to be unassigned from it, then assigned the new one.

                db_cursor.execute("""
                INSERT INTO hrapp_employeecomputer (assigned_date, computer_id, employee_id)
                VALUES (?, ?, ?)
                """,
                (
                    datetime.today().strftime('%Y-%m-%d'), form_data['computer'], employee_id,
                ))

            return redirect(reverse('hrapp:employee', kwargs={'employee_id': employee_id}))
