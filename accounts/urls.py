from django.urls import path
from accounts import views

urlpatterns = [
    path('waiting-list/', views.WaitingListViewSet.as_view({'post': 'create'}), name='waiting-list'),
]
