import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Employee, Department
from hrapp.models import model_factory
from ..connection import Connection

# def create_department(cursor, row):
#     _row = sqlite3.Row(cursor, row)

#     department = Department()
#     department.id = _row['department_id']
#     department.name = _row['name']
#     department.budget = _row['budget']

#     employee = Employee()
#     employee.id = _row['id']
#     employee.first_name = _row['first_name']
#     employee.last_name = _row['last_name']
#     employee.department_id = _row['department_id']

#     department.employee = []

#     return (department, employee,)


def get_department(department_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            d.id,
            d.name,
            d.budget,
            e.id,
            e.first_name,
            e.last_name,
            e.department_id
        FROM hrapp_department d
        LEFT JOIN hrapp_employee e ON d.id = e.department_id
        where d.id = ?
        """, (department_id,))

        data =  db_cursor.fetchall()

        department_check = []
        employee_group = []
        for row in data:
            if(len(department_check) == 0):
                department = Department()
                department.id = row['department_id']
                department.name = row['name']
                department.budget = row['budget']
                department_check.append(department)

            employee = Employee()
            employee.id = row['id']
            employee.first_name = row['first_name']
            employee.last_name = row['last_name']
            employee.department_id = row['department_id']
            employee_group.append(employee)


        department_obj = {}
        
        department_obj["department"] = department_check[0]
        department_obj["employees"] = employee_group
        return department_obj

        # for(department, employee) in departments:
        #     if department.id not in department_employee:
        #         department_employee[department.id] = department
        #         department_employee[department.id].employees.append(employee)
        #     else:
        #         department_employee[department.id].employees.append(employee)


@login_required
def department_details(request, department_id):
    if request.method == 'GET':
        department = get_department(department_id)

        template = 'departments/department_detail.html'
        context = {
            'department': department["department"],
            'employees': department["employees"]
        }

        return render(request, template, context)