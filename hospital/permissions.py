# permissions.py

from rest_framework import permissions

from hospital.models import Hospital


class MembershipPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if 'hospital_slug' in view.kwargs:
            hospital = Hospital.objects.get(slug=view.kwargs['hospital_slug'])
            if hospital.user == request.user:
                return True
            return request.user in hospital.departments.all().values_list('employee')
        return False
