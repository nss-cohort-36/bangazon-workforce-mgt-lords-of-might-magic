import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer, Employee
from ..connection import Connection



def get_employees():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            e.first_name, 
            e.last_name, 
            e.id
	    from hrapp_employee e
        EXCEPT
        SELECT 
            e.first_name, 
            e.last_name, 
            e.id
	    from hrapp_employee e
	    LEFT JOIN hrapp_employeecomputer ec
	    WHERE ec.employee_id = e.id 
	    AND unassigned_date is NULL
        """)

        employee_data = db_cursor.fetchall()
        unassigned_employees = []

        for employee in employee_data:
            single_employee = Employee
            single_employee.first_name = employee['first_name']
            single_employee.last_name = employee['last_name']
            single_employee.id = employee['id']
            unassigned_employees.append(single_employee)

        return unassigned_employees


@login_required
def computer_form(request):
    if request.method == 'GET':
        employees = get_employees()
        template = 'computers/form.html'
        context = {
            'employees': employees
        }

        return render(request, template, context)

# @login_required
# def book_edit_form(request, book_id):

#     if request.method == 'GET':
#         book = get_book(book_id)
#         libraries = get_libraries()

#         template = 'books/form.html'
#         context = {
#             'book': book,
#             'all_libraries': libraries
#         }

#         return render(request, template, context)