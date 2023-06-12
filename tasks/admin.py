from django.contrib import admin
from .models import Task
# Register your models here.
# Acceso al panel admin django

class TaskAdmin(admin.ModelAdmin): # campo de lectura idnica la fecha del momento
    readonly_fields = ("created", )

admin.site.register(Task, TaskAdmin)