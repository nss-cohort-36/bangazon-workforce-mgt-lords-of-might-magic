import sqlite3
import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from hrapp.models import TrainingProgram
from ..connection import Connection

def past_training_list(request):
    pass
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                *
            from hrapp_trainingprogram ht
            """)

            past_programs = []
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

                if(row['start_date'] < current_date):
                    past_programs.append(training_program)

        template = 'training_programs/past_training_list.html'
        context = {
            'trainings': past_programs
        }

        return render(request, template, context)