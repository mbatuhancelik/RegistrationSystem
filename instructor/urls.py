from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('viewClassrooms', views.viewClassrooms, name='viewClassrooms'),
    path('filterClassrooms', views.filterClassrooms, name='filterClassrooms'),
    path('addCourse', views.addCourse, name='addCourse'),
    path('addCourseForm', views.addCourseForm, name='addCourseForm'),
    path('addPreq', views.addPreq, name='addPreq'),
    path('addPreqForm', views.addPreqForm, name='addPreqForm'),
    path('viewCourses', views.viewCourses, name='viewCourses'),
]