from rest_framework import serializers
from .models import JwtToken


class JwtTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = JwtToken
        fields = '__all__'
