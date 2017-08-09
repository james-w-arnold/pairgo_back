from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class EmployeeInviteSerializer(serializers.Serializer):
    emails = EmailSerializer(many=True)
    team = serializers.IntegerField()
    company = serializers.CharField(max_length=255)