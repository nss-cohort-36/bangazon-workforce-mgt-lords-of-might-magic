import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..connection import Connection



def get_training(training_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            *
        from hrapp_trainingprogram ht
        WHERE ht.id = ?
        """, (training_id,))

        return db_cursor.fetchone()


@login_required
def training_form(request):
    if request.method == 'GET':
        template = 'training_programs/training_form.html'
        

        return render(request, template)


@login_required
def training_edit_form(request, training_id):

    if request.method == 'GET':
        training = get_training(training_id)

        template = 'training_programs/training_form.html'
        context = {
            'training': training,
        }

        return render(request, template, context)