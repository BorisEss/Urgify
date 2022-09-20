from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from hospital import models
from hospital import serializers


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = models.Hospital.objects.all()
    serializer_class = serializers.HospitalSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer

    def perform_create(self, serializer):
        hospital_id = get_object_or_404(models.Hospital, slug=self.kwargs['hospital_slug'])
        serializer.save(hospital=hospital_id)
