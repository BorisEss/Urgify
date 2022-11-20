from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from accounts.models import WaitingList, Account
from accounts.serializers import WaitingListSerializer, AccountSerializer


class WaitingListViewSet(viewsets.ModelViewSet):
    queryset = WaitingList.objects.all()
    serializer_class = WaitingListSerializer
    permission_classes = [AllowAny]
    throttle_scope = 'waiting-list'


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user).order_by('name')
