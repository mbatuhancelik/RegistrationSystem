from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses', views.listCourses, name='courses'),
    path('enrollCourses', views.enrollCourse, name='enrollCourse'),
    path('transcript', views.transcript, name='transcript'),
    path('searchCourse', views.searchCourse, name='searchCourse'),
    path('filterCourses', views.filterCourses, name='filterCourses'),
]