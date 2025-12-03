import datetime

from audioop import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from .forms import RegistrationForm, RequestForm, ChangeStatusForm
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

class CreateCategoryView(LoginRequiredMixin, UserIsStaffRequired, CreateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('admin_categories')

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

@login_required
def update_request_view(request, pk):
    requestInst = get_object_or_404(Request, pk=pk)
    if request.user.is_staff and requestInst.status == 'n':
        if request.method == 'POST':
            form = ChangeStatusForm(request.POST, request.FILES)
            if form.is_valid():
                if form.cleaned_data['status'] == 'o':
                    requestInst.status = 'o'
                    requestInst.commentary = form.cleaned_data['commentary']
                    requestInst.updated_at = datetime.datetime.now()
                    requestInst.save()
                elif form.cleaned_data['status'] == 'd':
                    requestInst.status = 'd'
                    requestInst.photo_after = form.cleaned_data['photo_after']
                    requestInst.save()
                return redirect('admin_requests')
        else:
            form = ChangeStatusForm(instance=requestInst)
        return render(request, 'catalog/request_update.html', {'form': form})
    else:
        return redirect('index')
