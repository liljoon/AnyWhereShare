from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'username', 'email', 'password']

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise ValidationError('이미 사용 중인 아이디입니다.')
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError('이미 사용 중인 이메일입니다.')
        return data

    def create(self, validated_data):
        user = User.objects.create(
            userId=validated_data['userId'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            accountType='RE',
        )
        return user
