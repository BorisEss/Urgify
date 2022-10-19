from rest_framework import serializers

from accounts import models


class WaitingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WaitingList
        fields = ('email',)


class InviteMemberSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=55)
    last_name = serializers.CharField(max_length=55)
    email = serializers.EmailField()
    phone = serializers.CharField(required=False)
