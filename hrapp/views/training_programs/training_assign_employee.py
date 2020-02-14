import sqlite3
import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from hrapp.models import TrainingProgram
from ..connection import Connection


def training_program_assign_employee(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                *
            from hrapp_trainingprogram ht
            """)

            upcoming_programs = []
            dataset = db_cursor.fetchall()

            d = datetime.datetime.today()
            current_date = str(d).split(' ')[0]
            for row in dataset:
                if(row['start_date'] > current_date):
                    training_program = TrainingProgram()
                    training_program.id = row['id']
                    training_program.title = row['title']
                    upcoming_programs.append(training_program)

            template = 'training_programs/training_assign.html'
        context = {
            'trainings': upcoming_programs
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_trainingprogramemployee
            (
                make, purchase_date
            )
            VALUES (?, ?)
            """,
            (form_data['make'], today))

        return redirect(reverse('hrapp:computers'))