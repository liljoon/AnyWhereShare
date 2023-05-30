from rest_framework import serializers
from .models import sharing

class sharingSerializer(serializers.ModelSerializer):
	class Meta:
		model = sharing
		fields = ('__all__')
