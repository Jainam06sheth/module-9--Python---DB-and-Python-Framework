from django.contrib import admin
from .models import Doctor

# Register your models here.


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'speciality', 'experience')
    search_fields = ('name',)

admin.site.register(Doctor, DoctorAdmin)