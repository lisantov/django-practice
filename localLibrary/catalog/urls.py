from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
]

urlpatterns += [
    re_path(r'^books/$', views.BookListView.as_view(), name='books'),
    re_path(r'^books/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
]

urlpatterns += [
    re_path(r'^author/$', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [
    re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    re_path(r'^borrowedbooks/$', views.LoanedBooksListView.as_view(), name='borrowed'),
]