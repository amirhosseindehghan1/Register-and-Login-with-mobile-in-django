from django.contrib import admin
from .models import MyUser
from import_export.admin import ExportActionMixin
# Register your models here.

class Myuser_Admin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('mobile', 'first_name', 'last_name', 'email')
    search_fields = ('mobile', 'email', 'first_name', 'last_name')


admin.site.register(MyUser, Myuser_Admin)