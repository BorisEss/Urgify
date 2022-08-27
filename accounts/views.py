from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from accounts import models
from accounts import serializers


class WaitingListViewSet(viewsets.ModelViewSet):
    queryset = models.WaitingList.objects.all()
    serializer_class = serializers.WaitingListSerializer
    permission_classes = [AllowAny]
    throttle_scope = 'waiting-list'
