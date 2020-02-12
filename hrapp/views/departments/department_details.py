import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import employee, Department
from hrapp.models import model_factory
from ..connection import Connection

def get_department(department_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Department)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            d.id,
            d.name,
            d.budget
        FROM hrapp_department d
        where d.id = ?
        """, (department_id,))

        return db_cursor.fetchone()

@login_required
def department_details(request, department_id):
    if request.method == 'GET':
        department = get_department(department_id)

        template = 'departments/department_detail.html'
        context = {
            'department': department
        }

        return render(request, template, context)