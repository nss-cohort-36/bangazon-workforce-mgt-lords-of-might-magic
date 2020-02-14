import sqlite3
import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from hrapp.models import TrainingProgram
from ..connection import Connection

def training_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                *
            from hrapp_trainingprogram ht
            """)

            all_programs = []
            dataset = db_cursor.fetchall()

            d = datetime.datetime.today()
            current_date = str(d).split(' ')[0]
            for row in dataset:
                training_program = TrainingProgram()
                training_program.id = row['id']
                training_program.title = row['title']
                training_program.description = row['description']
                training_program.start_date = row['start_date']
                training_program.end_date = row['end_date']
                training_program.capacity = row['capacity']

                if(row['start_date'] > current_date):
                    all_programs.append(training_program)

        if request.user.is_authenticated:
            template = 'training_programs/training_list.html'
        else:
            template = 'training_programs/training_list_view_only.html'

        context = {
            'trainings': all_programs
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_trainingprogram
            (
            title, description, start_date, end_date, capacity
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (form_data['title'], form_data['description'], form_data['start_date'], form_data['end_date'], form_data['capacity']))

        return redirect(reverse('hrapp:training_list'))