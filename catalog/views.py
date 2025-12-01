from django.contrib.auth import login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .forms import RegistrationForm
from .models import Request

def index(request):
    num_ongoing = Request.objects.filter(status__exact='o').count()
    last_done = Request.objects.filter(status__exact='d')[:4]

    context = {
        'num_ongoing': num_ongoing,
        'last_done': last_done,
    }

    return render(request, 'catalog/index.html', context=context)

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

class RequestCreate(PermissionRequiredMixin, CreateView):
    model = Request
    fields = ['title', 'description', 'category', 'photo']
    permission_required = 'catalog.add_request'