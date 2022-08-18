from rest_framework import serializers

from hospital import models


class HospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Hospital
        fields = ('name', 'slug', 'logo')


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Department
        fields = ('name', 'slug', 'hospital_id')
