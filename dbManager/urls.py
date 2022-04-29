from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addStudentForm', views.addStudentForm, name='addStudentForm'),
    path('addStudent', views.addStudent, name='addStudent'),
    path('addInstructorForm', views.addInstructorForm, name='addInstructorForm'),
    path('addInstructor', views.addInstructor, name='addInstructor')
]