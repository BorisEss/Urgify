from django.contrib import admin

from hospital.models import Employee, Hospital, Department

admin.site.register(Employee)
admin.site.register(Hospital)
admin.site.register(Department)
