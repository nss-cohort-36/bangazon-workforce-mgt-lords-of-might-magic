import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer
from ..connection import Connection


def get_computer(computer_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            SELECT 
            c.id, 
            c.make, 
            c.purchase_date, 
            c.decommission_date, 
            ec.unassigned_date, 
            e.id, 
            e.first_name, 
            e.last_name
	    from hrapp_computer c
	    left join hrapp_employeecomputer ec
	    on c.id = ec.computer_id
	    left JOIN hrapp_employee e
	    ON ec.employee_id = e.id
        WHERE c.id = ?
        """, (computer_id,))

        computer_data = db_cursor.fetchone()

        computer = Computer()
        computer.id = computer_data['id']
        computer.make = computer_data['make']
        computer.purchase_date = computer_data['purchase_date']
        computer.decommission_date = computer_data['decommission_date']
        if computer_data['unassigned_date'] is None:
            if computer_data["first_name"] is not None:
                computer.current_user = f"{computer_data['first_name']} {computer_data['last_name']}"
            else:
                computer.current_user = "Unassigned"
        else:
            computer.current_user = "Unassigned"
        return computer

@login_required
def computer_details(request, computer_id):
    if request.method == 'GET':
        computer = get_computer(computer_id)

        template = 'computers/details.html'
        context = {
            'computer': computer
        }

        return render(request, template, context)

    # if request.method == 'POST':
    #     form_data = request.POST
    #     # Check if this POST is for editing a book
    #     if (
    #         "actual_method" in form_data
    #         and form_data["actual_method"] == "PUT"
    #     ):
    #         with sqlite3.connect(Connection.db_path) as conn:
    #             db_cursor = conn.cursor()

    #             db_cursor.execute("""
    #             UPDATE libraryapp_book
    #             SET title = ?,
    #                 author = ?,
    #                 ISBN_number = ?,
    #                 year_published = ?,
    #                 location_id = ?
    #             WHERE id = ?
    #             """,
    #             (
    #                 form_data['title'], form_data['author'],
    #                 form_data['isbn'], form_data['year_published'],
    #                 form_data["location"], book_id,
    #             ))

    #         return redirect(reverse('libraryapp:books'))
    #     # Check if this POST is for deleting a book
    #     #
    #     # Note: You can use parenthesis to break up complex
    #     #       `if` statements for higher readability
    #     if (
    #         "actual_method" in form_data
    #         and form_data["actual_method"] == "DELETE"
    #     ):
    #         with sqlite3.connect(Connection.db_path) as conn:
    #             db_cursor = conn.cursor()

    #             db_cursor.execute("""
    #             DELETE FROM libraryapp_book
    #             WHERE id = ?
    #             """, (book_id,))

    #         return redirect(reverse('libraryapp:books'))


