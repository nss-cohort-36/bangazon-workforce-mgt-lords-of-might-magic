import sqlite3
from django.shortcuts import render, redirect, reverse
from hrapp.models import Department
from ..connection import Connection


def department_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                d.id,
                d.name,
                d.budget,
                e.id AS 'employee_id'
            FROM hrapp_department d
            LEFT JOIN hrapp_employee e
            ON d.id = e.department_id
            """)

            all_departments = []
            dataset = db_cursor.fetchall()

            # creates a list of all unique department objects
            for row in dataset:
                department = Department()
                department.id = row['id']
                department.name = row['name']
                department.budget = row['budget']
                if(department not in all_departments):
                    all_departments.append(department)

            # creates a dictionary of all unique department names with values representing employee count
            department_sizes = dict()
            for row in dataset:
                if(row['name'] not in department_sizes):
                    name = row['name']
                    department_sizes[name] = 0

            # and here we set the employee count for each department
            for row in dataset:
                if(row['employee_id'] is not None):
                    name = row['name']
                    department_sizes[name] += 1

            # transfer the department sizes to the department objects in all_departments
            for department in all_departments:
                department.size = department_sizes[department.name]

        template = 'departments/department_list.html'
        context = {
            'departments': all_departments
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT into hrapp_department
            (
                name, budget
            )
            VALUES (?, ?)
            """,
            (form_data['name'], form_data['budget']))

        return redirect(reverse('hrapp:department_list'))