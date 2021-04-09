from django.shortcuts import render


# Create your views here.
def render_template(request, index=None):
    return render(request, 'ServiceCenter/search_app.html')
