from django.contrib import admin
from accounts.models import User, MemberInvite

admin.site.register(User)
admin.site.register(MemberInvite)
