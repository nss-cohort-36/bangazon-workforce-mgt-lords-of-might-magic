import sqlite3
import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from hrapp.models import TrainingProgram
from ..connection import Connection


def training_program_assign_employee(request, employee_id):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                *
            from hrapp_trainingprogram ht
            EXCEPT
            SELECT tr.*
            FROM hrapp_trainingprogram tr
            LEFT JOIN hrapp_trainingprogramemployee te
            ON tr.id = te.training_program_id
            WHERE te.employee_id = ?
            """,
            (str(employee_id),))

            upcoming_programs = []
            dataset = db_cursor.fetchall()

            d = datetime.datetime.today()
            current_date = str(d).split(' ')[0]
            for row in dataset:
                if(row['start_date'] > current_date):
                    training_program = TrainingProgram()
                    training_program.id = row['id']
                    training_program.title = row['title']
                    training_program.start_date = row['start_date']
                    training_program.end_date = row['end_date']
                    upcoming_programs.append(training_program)

            template = 'employees/employee_assign_training.html'
            context = {
                'trainings': upcoming_programs,
                'employee_id': employee_id
            }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_trainingprogramemployee
            (
                employee_id, training_program_id
            )
            VALUES (?, ?)
            """,
            (employee_id, form_data['training']))

        return redirect(reverse('hrapp:employee_list'))