from rest_framework import serializers
from .models import GuestUser, FileInfo

class GuestUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = GuestUser
		fields = '__all__'

class FilesListSerializer(serializers.ModelSerializer):
	created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

	class Meta:
		model = FileInfo
		fields = '__all__'
