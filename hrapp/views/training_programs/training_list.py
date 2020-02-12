import sqlite3
from django.shortcuts import render
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

            for row in dataset:
                training_program = TrainingProgram()
                training_program.id = row['id']
                training_program.title = row['title']
                training_program.start_date = row['start_date']
                training_program.end_date = row['end_date']
                training_program.capacity = row['capacity']

                all_programs.append(training_program)

        template = 'training_programs/training_list.html'
        context = {
            'all_programs': all_programs
        }

        return render(request, template, context)