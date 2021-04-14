from django.urls import path

from ServiceCenter.views import render_template, Category, Products_view, get_product_by_category

urlpatterns = [
    path('template', render_template, name='index'),
    path('ajax_category', Category.as_view(), name='ajax_category'),
    path('ajax_product', Products_view.as_view(), name='ajax_product'),
    path('ajax_category_product', get_product_by_category, name='ajax_category_product'),

]
