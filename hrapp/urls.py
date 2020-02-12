from django.urls import path, reverse
from django.conf.urls import include
from hrapp import views
from .views import *

app_name = 'hrapp'
urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('computers/', computer_list, name='computers'),
    path('computers/form', computer_form, name='computer_form'),
    path('computers/<int:computer_id>/', computer_details, name='computer_details'),
    path('computers/delete/<int:computer_id>', computer_delete, name='computer_delete'),
    path('employees/', employee_list, name='employee_list'),
    path('trainings/', training_list, name='training_list'),
    path('trainings/form', training_form, name='training_form'),
    path('employees/form', employee_form, name='employee_form'),
    path('departments/', department_list, name='department_list'),
]
