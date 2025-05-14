from django.contrib import admin
from .models import User
# Register your models here.


@admin.register(User)   
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'user_roles', 'created_at', 'updated_at')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('user_roles', 'created_at', 'updated_at')
    ordering = ('-created_at',)