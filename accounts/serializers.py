from rest_framework import serializers

from accounts import models


class WaitingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WaitingList
        fields = ('email',)
