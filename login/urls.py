from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('databaseManagerLogin',views.databaseManagerLogin,name="databaseManagerLogin"),
    path('lecturerLogin',views.lecturerLogin,name="lecturerLogin"),
    path('studentLogin',views.studentLogin,name="studentLogin"),
]