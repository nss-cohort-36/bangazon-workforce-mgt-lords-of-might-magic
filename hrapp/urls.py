from django.urls import path
from django.conf.urls import include
from hrapp import views
from .views import *

app_name = 'hrapp'
urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('employees/', employee_list, name='employee_list'),
    path('employees/<int:employee_id>/', employee_details, name='employee'),
    path('trainings/', training_list, name='training_list'),
    path('trainings/form', training_form, name='training_form'),
    path('employees/form', employee_form, name='employee_form'),
    path('departments/', department_list, name='department_list'),
]
