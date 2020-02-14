import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import Department, Computer, model_factory
from .employee_details import get_employee
from ..connection import Connection


def get_departments():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Department)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            d.id,
            d.name
        FROM hrapp_department d
        """)

        return db_cursor.fetchall()


def get_avail_computers():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Computer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.make,
            e.first_name
        FROM
            hrapp_computer c
            LEFT JOIN hrapp_employeecomputer ec ON c.id = ec.computer_id
            LEFT JOIN hrapp_employee e ON e.id = ec.employee_id
        WHERE
            c.decommission_date IS NULL;
        """)

        print(db_cursor)

        return db_cursor.fetchall()

@login_required
def employee_form(request):
    if request.method == 'GET':
        departments = get_departments()
        template = 'employees/employees_form.html'
        context = {
            'all_departments': departments
        }

        return render(request, template, context)

@login_required
def employee_edit_form(request, employee_id):
    if request.method == 'GET':
        employee = get_employee(employee_id)
        departments = get_departments()
        computers = get_avail_computers()
        print(computers)
        template = 'employees/employees_form.html'
        context = {
            'employee': employee,
            'all_departments': departments,
            'all_computers': computers
        }

        return render(request, template, context)
