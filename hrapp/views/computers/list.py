import sqlite3
import datetime
from django.shortcuts import render, redirect, reverse
from hrapp.models import Computer
from ..connection import Connection


def computer_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            
            db_cursor.execute("""
            SELECT 
                c.id, 
                c.make
	        from hrapp_computer c
            """)

            all_computers = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                computer = Computer()
                computer.id = row['id']
                computer.make = row['make']
                # computer.purchase_date = row['purchase_date']
                # computer.decommission_date = row['decommission_date']
                # if row['unassigned_date'] is None:
                #     if row["first_name"] is not None:
                #         computer.current_user = f"{row['first_name']} {row['last_name']}"
                #     else:
                #         computer.current_user = "Unassigned"
                # else:
                #     computer.current_user = "Unassigned"
                all_computers.append(computer)

        template = 'computers/list.html'
        context = {
            'computers': all_computers
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            today = datetime.datetime.today()

            db_cursor.execute("""
            INSERT INTO hrapp_computer
            (
                make, purchase_date
            )
            VALUES (?, ?)
            """,
            (form_data['make'], today))

        return redirect(reverse('hrapp:computers'))
