from rest_framework import serializers
from .models import *


class ReferalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferFriend
        fields = '__all__'