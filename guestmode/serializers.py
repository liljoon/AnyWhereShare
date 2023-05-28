from rest_framework import serializers
from .models import GuestUser

class GuestUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = GuestUser
		fields = '__all__'
