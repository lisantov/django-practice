from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]

urlpatterns += [
    path('author/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]