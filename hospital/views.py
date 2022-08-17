from rest_framework import viewsets

from hospital import models
from hospital import serializers


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = models.Hospital.objects.all()
    serializer_class = serializers.HospitalSerializer
