from django.shortcuts import render


# Create your views here.
from vue_utils.views import FilterAjaxListView

from Product.models import Categories


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