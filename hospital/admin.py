from django.contrib import admin

from hospital.models import Employee, Hospital, Department

admin.site.register(Hospital)
admin.site.register(Department)


@admin.register(Employee)
class MemberInviteAdmin(admin.ModelAdmin):
    list_display = ('user', 'attribution', 'status', 'department')
