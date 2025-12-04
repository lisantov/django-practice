from django.urls.conf import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('snippets/', views.SnippetList.as_view(), name='snippet_list'),
    path('snippets/<int:pk>', views.SnippetDetail.as_view(), name='snippet_detail'),
    path('users/', views.UserList.as_view(), name='snippet_list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='snippet_detail'),
    path('auth/', include('rest_framework.urls'), name='auth'),
]

urlpatterns = format_suffix_patterns(urlpatterns)