import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def computer_delete(request, computer_id):
    if request.method == 'POST':
        print(computer_id)
        template = 'computers/delete.html'
        context = {
            'computer_id': computer_id
        }

        return render(request, template, context)