from rest_framework import serializers

class IndustrySerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return str(instance.name)
    def to_internal_value(self, data):
        return data
