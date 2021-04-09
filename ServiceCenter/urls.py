from django.urls import path

from ServiceCenter.views import render_template, Category

urlpatterns = [
    path('template', render_template, name='index'),
    path('ajax_category', Category.as_view(), name='ajax_category'),
]
