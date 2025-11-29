from django.contrib import admin
from .models import AdvancedUser, Request, Category


@admin.register(AdvancedUser)
class AdvancedUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'fio')

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'updated_at', 'created_at')

admin.site.register(Category)