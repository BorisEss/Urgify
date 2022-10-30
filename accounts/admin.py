from django.contrib import admin
from accounts.models import User, MemberInvite


@admin.register(MemberInvite)
class MemberInviteAdmin(admin.ModelAdmin):
    list_display = ('invitee', 'sender', 'status', 'department')


admin.site.register(User)
