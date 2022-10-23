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

department_detail = views.DepartmentViewSet.as_view({
    'delete': 'destroy',
})

employee_list = views.EmployeeViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    path('', hospital_list, name='hospital-list'),
    path('<slug:slug>/', hospital_detail, name='hospital-detail'),
    path('<slug:hospital_slug>/departments/', department_list, name='department-list'),
    path('<slug:hospital_slug>/departments/<slug:slug>/', department_detail, name='department-detail'),
    path('<slug:hospital_slug>/departments/<slug:department_slug>/employee/', employee_list, name='employee-list'),
]
