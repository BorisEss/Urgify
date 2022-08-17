from django.urls import path
from hospital import views

hospital_list = views.HospitalViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = [
    path('', hospital_list, name='hospital-list'),
]
