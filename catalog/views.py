from audioop import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from .forms import RegistrationForm, RequestForm
from .models import Request, Category
from .staff_mixin import UserIsStaffRequired


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

@login_required
def create_request_view(request):
    current_user = request.user
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            request = form.save(commit=False)
            request.author = current_user
            request.save()
            return redirect('user_requests')
    else:
        form = RequestForm()
    return render(request, 'catalog/request_form.html', {'form': form})

class UserRequestsView(LoginRequiredMixin, ListView):
    model = Request
    context_object_name = 'requests_list'
    template_name = 'catalog/user_requests.html'

    def get_queryset(self):
        return ({
            'requests': Request.objects.filter(author=self.request.user)
        })

class UserRequestsFilterView(LoginRequiredMixin, ListView):
    model = Request
    context_object_name = 'requests_list'
    template_name = 'catalog/user_requests.html'

    def get_queryset(self):
        return ({
            'requests': Request.objects.filter(author=self.request.user).filter(status__exact=self.kwargs['filter']),
            'filter': self.kwargs['filter']
        })

class DeleteRequestView(LoginRequiredMixin, DeleteView):
    model = Request
    success_url = reverse_lazy('user_requests')

    def form_valid(self, form):
        try:
            if self.request.user.is_staff or self.request.user == self.object.author:
                self.object.delete()
                return redirect('user_requests')
            else:
                return HttpResponseForbidden('У вас нету доступа для этого действия')
        except Exception as e:
            return HttpResponseRedirect(reverse("delete_request", kwargs={'pk': self.object.pk}))

class AdminCategoriesView(LoginRequiredMixin, UserIsStaffRequired, ListView):
    model = Category
    context_object_name = 'categories_list'
    template_name = 'catalog/admin_categories.html'

class DeleteCategoryView(LoginRequiredMixin, UserIsStaffRequired, DeleteView):
    model = Category

    def form_valid(self, form):
        try:
            self.object.delete()
            return redirect('admin_categories')
        except Exception as e:
            return HttpResponseRedirect(reverse("delete_category", kwargs={'pk': self.object.pk}))

class AdminRequestsView(LoginRequiredMixin, UserIsStaffRequired, ListView):
    model = Request
    context_object_name = 'requests_list'
    template_name = 'catalog/admin_requests.html'

    def get_queryset(self):
        return ({
            'requests': Request.objects.all,
        })

class AdminRequestsFilterView(LoginRequiredMixin, UserIsStaffRequired, ListView):
    model = Request
    context_object_name = 'requests_list'
    template_name = 'catalog/admin_requests.html'

    def get_queryset(self):
        return ({
            'requests': Request.objects.filter(status__exact=self.kwargs['filter']),
            'filter': self.kwargs['filter']
        })