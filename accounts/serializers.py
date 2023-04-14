from rest_framework import serializers
from .models import Account

class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'userId',
            'username',
            'email',
            'accountType',
            'password',
            'url']