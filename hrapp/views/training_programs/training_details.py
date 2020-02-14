import sqlite3
import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from hrapp.models import TrainingProgram
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

def get_training_attendees(training_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            tpe.id,
            tpe.employee_id,
            tpe.training_program_id,
            e.first_name,
            e.last_name
        FROM hrapp_trainingprogramemployee tpe
        JOIN hrapp_employee e
        ON tpe.employee_id = e.id
        WHERE tpe.training_program_id = ?
        """, (training_id,))

        return db_cursor.fetchall()


def training_details(request, training_id):
    if request.method == 'GET':
        d = datetime.datetime.today()
        current_date = str(d).split(' ')[0]

        training = get_training(training_id)
        attendees = get_training_attendees(training_id)

        if(training['start_date'] < current_date):
            template = 'training_programs/past_training_details.html'
        else:
            template = 'training_programs/training_details.html'

        context = {
            'attendees': attendees,
            'training': training
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE hrapp_trainingprogram
                SET title = ?,
                    description = ?,
                    start_date = ?,
                    end_date = ?,
                    capacity = ?
                WHERE id = ?
                """,
                (
                    form_data['title'], form_data['description'], form_data['start_date'], form_data['end_date'], form_data['capacity'], training_id,
                ))

            return redirect(reverse('hrapp:training_list'))

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
         ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM hrapp_trainingprogram
                WHERE id = ?
                """, (training_id,))

        return redirect(reverse('hrapp:training_list'))