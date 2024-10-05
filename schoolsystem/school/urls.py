from django.urls import path
from school.views import user_login
from school.views import Dashboard
from school.views import register
from .views import student_list,add_student,edit_student,delete_student, student_search


urlpatterns = [
     path('', user_login, name='/pages/loginpage'),
     path('dashboard', Dashboard, name='/pages/dashboard'),
     path('register', register, name='/pages/register'),
      path('students/', student_list, name='student_list'),
    path('students/add/', add_student, name='add_student'),
    path('students/edit/<int:student_id>/', edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', delete_student, name='delete_student'),
      path('student/search/', student_search, name='student_search'),
]