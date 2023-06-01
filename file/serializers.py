from rest_framework import serializers
from .models import Resource
from django.core.exceptions import ValidationError


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'
