from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('user/requests/', views.UserRequestsView.as_view(), name='user_requests'),
    path('request/create/', views.create_request_view, name='create_request'),
    path('request/delete/<int:pk>', views.DeleteRequestView.as_view(), name='delete_request'),
]
