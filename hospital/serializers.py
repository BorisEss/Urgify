from rest_framework import serializers

from hospital import models


class HospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Hospital
        fields = ('name', 'slug', 'logo')
