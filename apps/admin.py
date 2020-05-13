from django.contrib import admin

# Register your models here.
from apps.models import UserInfo, Employee

admin.site.register(UserInfo)
admin.site.register(Employee)