from django.urls import path

from accounts.views import WaitingListViewSet, AccountViewSet

account_list = AccountViewSet.as_view({
    'post': 'create',
})

account_detail = AccountViewSet.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    path('', account_list, name='account-list'),
    path('<slug:slug>/', account_detail, name='account-detail'),
    path('waiting-list/', WaitingListViewSet.as_view({'post': 'create'}), name='waiting-list'),
]
