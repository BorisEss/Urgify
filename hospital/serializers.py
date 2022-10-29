from rest_framework import serializers
from django.utils.translation import gettext as _

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
            raise serializers.ValidationError(_('Department name must be unique in context of hospital'))
        return value


class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    attribution = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = models.Employee
        fields = '__all__'

    def get_attribution(self, instance):
        return instance.get_attribution_display()

    def get_status(self, instance):
        return instance.get_status_display()

    def get_email(self, instance):
        return instance.user.email
