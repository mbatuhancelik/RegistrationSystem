from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('viewClassrooms', views.viewClassrooms, name='viewClassrooms'),
    path('filterClassrooms', views.filterClassrooms, name='filterClassrooms'),
]