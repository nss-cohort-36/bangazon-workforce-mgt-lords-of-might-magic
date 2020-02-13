from .home import home
from .auth.logout import logout_user

from .employees.employee_list import employee_list
from .employees.employee_form import employee_form
from .employees.employee_details import employee_details

from .computers.list import computer_list
from .computers.form import computer_form
from .computers.details import computer_details
from .computers.delete import computer_delete

from .training_programs.training_list import training_list
from .training_programs.training_form import training_form, training_edit_form
from .training_programs.training_details import training_details

from .departments.department_list import department_list
from .departments.department_details import department_details
from .departments.department_form import department_form
