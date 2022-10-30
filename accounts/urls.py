from django.urls import path
from accounts import views

urlpatterns = [
    path('waiting-list/', views.WaitingListViewSet.as_view({'post': 'create'}), name='waiting-list'),
    path('invite-member/<slug:hospital_slug>/<slug:department_slug>/', views.InviteMemberViewSet.as_view({'post': 'create'}), name='invite-member'),
    path('accept-invite-new-user/', views.AcceptInviteViewSet.as_view({'post': 'accept_invite_new_user'}), name='accept-invite-new-user'),
    path('accept-invite-existing-user/', views.AcceptInviteViewSet.as_view({'post': 'accept_invite_existing_user'}), name='accept-invite-existing-user'),
]
