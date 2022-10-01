from django.urls import path
from hospital import views

hospital_list = views.HospitalViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

hospital_detail = views.HospitalViewSet.as_view({
    'get': 'retrieve',
})

department_list = views.DepartmentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

employee_list = views.EmployeeViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = [
    path('', hospital_list, name='hospital-list'),
    path('<slug:slug>/', hospital_detail, name='hospital_detail'),
    path('<slug:hospital_slug>/departments/', department_list, name='department-list'),
    path('<slug:hospital_slug>/departments/<slug:department_slug>/employee/', employee_list, name='employee-list'),
]
