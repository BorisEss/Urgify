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

    def validate_name(self, value):
        hospital_slug = self.context.get('view').kwargs.get('hospital_slug')
        if models.Department.objects.filter(hospital__slug=hospital_slug, name=value).exists():
            raise serializers.ValidationError('Department name must be unique in context of hospital')
        return value


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Employee
        fields = ('attribution',)
