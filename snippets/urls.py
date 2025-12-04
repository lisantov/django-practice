from django.urls.conf import path, include

urlpatterns = [
    path('api/', include('api.urls')),
]