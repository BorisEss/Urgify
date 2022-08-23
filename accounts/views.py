from rest_framework import viewsets

from accounts import models
from accounts import serializers


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = models.WaitingList.objects.all()
    serializer_class = serializers.WaitingListSerializer
