from django.urls import path
from hospital import views

urlpatterns = [
    path('waiting-list/', views.HospitalViewSet.as_view({'post': 'create'}), name='waiting-list'),
]
