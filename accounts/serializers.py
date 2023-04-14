from .models import Account
from rest_framework import serializers


class AccountSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    def create(self, validated_data):
        user = Account.objects.create_user(
            userId=validated_data['userId'],
            password=validated_data['password'],
            username=validated_data['username'],
            email=validated_data['email'],
        )
        return user