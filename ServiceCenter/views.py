from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from vue_utils.request_processsor.utility import get_from_request
from vue_utils.request_processsor.view import filter_query
from vue_utils.views import FilterAjaxListView

from Product.models import Categories, Products


def render_template(request, index=None):
    return render(request, 'ServiceCenter/search_app.html')


class Category(FilterAjaxListView):
    model = Categories
    filters_fields = [
        'id',
        'name',
        'code',
        ('parent__id', None, 'level', None),
        ('parent__id', 'isnull', 'main', bool),
    ]
    serialized_fields = [
        ('id', None, 'key'),
        ('name', None, 'label'),
        ('code', None, 'data'),
        ('categories_set__count', 'bool_not', 'leaf'),
    ]


class Products_view(FilterAjaxListView):
    model = Products
    filters_fields = [
        'id',
        'name',
        'code',
        'product_code',
        'default_warranty',
        'default_price',
    ]


def get_product_by_category(request):
    category_id, _ = get_from_request(request, 'category_id', None)
    if category_id:
        category = Categories.objects.get(id=category_id)
        objects = category.products_set.all()
    else:
        objects = Products.objects.all()
    context = filter_query(request, objects, ['id',
                                              'name',
                                              'code',
                                              'product_code',
                                              'default_warranty',
                                              'default_price',
                                              'brand__code'
                                              ],
                           configuration={'use_combined_filter': 'view_filter', 'use_extended_filter': True})

    return JsonResponse(context, safe=False)
