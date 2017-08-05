from rest_framework import serializers
from commons.models import commons

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = commons.Industry
        exclude = ('id',)
