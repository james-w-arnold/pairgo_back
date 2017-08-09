from rest_framework import serializers
from .models import *
from employers.models import Team, Company
from accounts.serializers.serializers import LocationSerializer
from rest_framework.exceptions import ValidationError

class PostingInterestSerializer(serializers.Serializer):
    def to_representation(self, instance):
        posting_interests = PostingInterest.objects.filter(posting__id=instance.instance.id)
        interests = [interest.interest.name for interest in posting_interests]
        return interests
    def to_internal_value(self, data):
        interests = [interest for interest in data]
        return interests

class PostingSkillSerializer(serializers.Serializer):
    def to_representation(self, instance):
        posting_skills = PostingSkill.objects.filter(posting__id=instance.instance.id)
        skills = [skill.skill.name for skill in posting_skills]
        return skills
    def to_internal_value(self, data):
        return data

class PostingLocationSerializer(serializers.Serializer):
    def to_representation(self, instance):
        posting_locations = PostingLocation.objects.filter(posting__id=obj.instance.id)
        locations = []
        if posting_locations.exists():
            for location in posting_locations:
                serialized_location = (LocationSerializer(location.location)).data
                locations.append(serialized_location)
        return locations

    def to_internal_value(self, data):
        locations = []
        if data:
            for location in data:
                locations.append(PostingLocationSerializer.__parse_location(location))

    @staticmethod
    def __parse_location(location):

        data = {
            "title" : location.get('title', ''),
            "lat" : location.get('lat'),
            "lon" : location.get('lon')
        }
        serializer = LocationSerializer(data=data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            return validated_data
        else:
            return ValidationError('Incorreect Location data')

class PostingEmployeeSerializer(serializers.Serializer):
    def to_representation(self, instance):
        posting_employees = PostingEmployee.objects.filter(posting__id = instance.instance.id)
        employees = [{"fist_name" : employee.employee.user.first_name, "last_name" : employee.employee.user.last_name, "id" : employee.employee.id} for employee in posting_employees]
        return employees

    def to_internal_value(self, data):
        employee_ids = [emp_id.id for emp_id in data]
        return employee_ids

class PostingCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'company_name')


class PostingSerializer(serializers.ModelSerializer):
    """
    Serializer which controls the posting model
    """
    locations = PostingLocationSerializer(required=True)
    skills = PostingSkillSerializer()
    interests = PostingInterestSerializer()
    company = PostingCompanySerializer()
    employees = PostingEmployeeSerializer()

    class Meta:
        model = Posting
        exclude = ('psychometrics', )

