from django.contrib import admin
from .models import Patient
# Register your models here.

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'age', 'gender', 'phone', 'address', 'created_at', 'updated_at')
    list_filter = ('gender', 'age')
    search_fields = ('user__username', 'name', 'phone', 'address')
    ordering = ('-created_at',)
