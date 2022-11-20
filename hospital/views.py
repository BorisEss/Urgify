import logging

from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from tablib import Dataset
from django.utils.translation import gettext as _
from rest_framework import status
import tablib

from hospital import models
from hospital import serializers
from hospital.permissions import MembershipPermission
from hospital.importexport import PatientResource


class HospitalViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HospitalSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return models.Hospital.objects.filter(user=self.request.user).order_by('name')


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DepartmentSerializer
    permission_classes = (MembershipPermission,)
    lookup_field = 'slug'

    def get_queryset(self):
        return models.Department.objects\
            .filter(hospital__slug=self.kwargs['hospital_slug'])\
            .order_by('name')

    def perform_create(self, serializer):
        hospital = get_object_or_404(models.Hospital, slug=self.kwargs['hospital_slug'])
        serializer.save(hospital=hospital)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    permission_classes = (MembershipPermission,)
    serializer_class = serializers.EmployeeSerializer

    def get_queryset(self):
        return models.Employee.objects.filter(department__slug=self.kwargs['department_slug'])


class PatientViewSet(viewsets.GenericViewSet):

    def import_patients(self, request, hospital_slug):
        serializer = serializers.ImportPatientsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dataset = Dataset()
        file = serializer.validated_data['file']
        patient_resource = PatientResource()

        try:
            imported_data = dataset.load(file.read().decode('utf-8'), format='csv')
        except tablib.InvalidDimensions as e:
            logging.error(e, exc_info=True)
            return Response(_('Looks like your file does not fit the format'), status=status.HTTP_400_BAD_REQUEST)

        hospital_id = models.Hospital.objects.get(slug=hospital_slug).id
        data_arr = [hospital_id] * len(imported_data)

        imported_data.append_col(data_arr, header='hospital')
        result = patient_resource.import_data(dataset, dry_run=True)

        if result.has_errors():
            return Response('Uh oh! Something went wrong...', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            patient_resource.import_data(dataset, dry_run=False)
            return Response('success', status=status.HTTP_201_CREATED)
