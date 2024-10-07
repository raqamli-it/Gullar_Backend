from django.contrib import admin
from .models import AbstractUser, UserImage

class AbstractUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'role', 'is_superuser', 'is_active', 'created_at')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('full_name', 'phone')
    ordering = ('-created_at',)

admin.site.register(AbstractUser, AbstractUserAdmin)
admin.site.register(UserImage)

