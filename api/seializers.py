from rest_framework import serializers
from .models import ApiModel

class ApiSerializers (serializers.ModelSerializer):
    class Meta:
        model = ApiModel
        fields = ['id','image_uri', 'title']

