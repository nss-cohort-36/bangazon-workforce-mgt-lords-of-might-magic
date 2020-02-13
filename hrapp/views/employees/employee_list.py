import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from hrapp.models import Employee, Department
from ..connection import Connection


def create_employee(cursor, row):
    _row = sqlite3.Row(cursor, row)

    e = Employee()
    e.id = _row["id"]
    e.first_name = _row["first_name"]
    e.last_name = _row["last_name"]

    d = Department()
    d.name = _row["department"]

    e.department = d

    return e


def employee_list(request):
    if request.method == 'GET':
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
                d.name department
            FROM hrapp_employee e
            JOIN hrapp_department d ON e.department_id = d.id
            """)

            all_employees = db_cursor.fetchall()

        template = 'employees/employees_list.html'
        context = {
            'employees': all_employees
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT into hrapp_employee
            (
                first_name, last_name, start_date, is_supervisor, department_id
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (form_data['first_name'], form_data['last_name'], form_data['start_date'],
            form_data['is_supervisor'], form_data['department']))

        return redirect(reverse('hrapp:employee_list'))
