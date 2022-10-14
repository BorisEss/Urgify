from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from hospital import models
from hospital import serializers
from hospital.permissions import MembershipPermission


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = models.Hospital.objects.all()
    serializer_class = serializers.HospitalSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return models.Hospital.objects.filter(user=self.request.user)


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DepartmentSerializer
    permission_classes = (MembershipPermission,)
    lookup_field = 'slug'

    def get_queryset(self):
        return models.Department.objects.filter(hospital__slug=self.kwargs['hospital_slug'])

    def perform_create(self, serializer):
        hospital = get_object_or_404(models.Hospital, slug=self.kwargs['hospital_slug'])
        serializer.save(hospital=hospital)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer

    def get_queryset(self):
        return models.Employee.objects.filter(department__slug=self.kwargs['department_slug'])
