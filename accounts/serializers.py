from rest_framework import serializers

from accounts.models import Account, WaitingList


class WaitingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WaitingList
        fields = ('email',)


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('name', 'slug', 'logo')
