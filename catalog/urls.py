from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('user/requests/', views.UserRequestsView.as_view(), name='user_requests'),
    path('user/requests/<str:filter>/', views.UserRequestsFilterView.as_view(), name='user_filter_requests'),
    path('admin/categories/', views.AdminCategoriesView.as_view(), name='admin_categories'),
    path('admin/requests/', views.AdminRequestsView.as_view(), name='admin_requests'),
    path('admin/requests/<str:filter>/', views.AdminRequestsFilterView.as_view(), name='admin_filter_requests'),
    path('request/create/', views.create_request_view, name='create_request'),
    path('request/delete/<int:pk>', views.DeleteRequestView.as_view(), name='delete_request'),
    path('category/delete/<int:pk>', views.DeleteCategoryView.as_view(), name='delete_category'),
]
