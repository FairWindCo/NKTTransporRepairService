from django.urls import path

from ServiceCenter.views import render_template

urlpatterns = [
    path('template', render_template, name='index'),
]
