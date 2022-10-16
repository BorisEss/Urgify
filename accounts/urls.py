from django.urls import path
from accounts import views

urlpatterns = [
    path('waiting-list/', views.WaitingListViewSet.as_view({'post': 'create'}), name='waiting-list'),
    path('invite-member/<slug:hospital_slug>/<slug:department_slug>/', views.InviteMemberViewSet.as_view({'post': 'create'}), name='invite-member'),
    path('accept-invite/<str:hash>/', views.InviteMemberViewSet.as_view({'post': 'accept_invite'}), name='accept-invite'),
]
