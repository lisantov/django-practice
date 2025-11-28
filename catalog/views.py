from django.shortcuts import render
from .models import Request

def index(request):
    num_ongoing = Request.objects.filter(status__exact='o').count()
    last_done = Request.objects.filter(status__exact='d')[:4]

    context = {
        'num_ongoing': num_ongoing,
        'last_done': last_done,
    }

    return render(request, 'catalog/index.html', context=context)