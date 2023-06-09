from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError
import bcrypt


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'password']

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise ValidationError('이미 사용 중인 아이디입니다.')
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError('이미 사용 중인 이메일입니다.')
        return data

    def create(self, validated_data):
        password = bcrypt.hashpw(validated_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User.objects.create(
            user_id=validated_data['user_id'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            account_type='RE',
        )
        return user
