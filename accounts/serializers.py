from rest_framework import serializers
from .models import Account

class AccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['userId', 'password', 'username', 'email']

class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = '__all__'