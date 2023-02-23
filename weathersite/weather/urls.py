from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('history', views.history, name='history'),
    path('result', views.result, name='result'),
]