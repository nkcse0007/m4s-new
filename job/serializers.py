from rest_framework import serializers
from .models import *


class RequestTalentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestTalent
        fields = '__all__'


class SubmitJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmitJob
        fields = '__all__'


class SubmitCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmitCV
        fields = '__all__'


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"
