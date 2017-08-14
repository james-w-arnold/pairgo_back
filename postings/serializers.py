from rest_framework import serializers
from .models import *
from employers.models import Team, Company
from accounts.serializers.serializers import LocationSerializer
from rest_framework.exceptions import ValidationError
import logging
from postings import serializer_tools as st

global logger
logger = logging.getLogger(__name__)

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
        posting_locations = PostingLocation.objects.filter(posting__id=instance.instance.id)
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


        return locations

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
        fields = ('id', 'company_name', 'industries')


class PostingSerializer(serializers.ModelSerializer):
    """
    Serializer which controls the posting model
    """
    company = serializers.SlugRelatedField(queryset=Company.objects.all(),
                                           read_only=False,
                                           slug_field='id')
    locations = PostingLocationSerializer(required=True)
    skills = PostingSkillSerializer()
    interests = PostingInterestSerializer()
    employees = PostingEmployeeSerializer(required=False)

    class Meta:
        model = Posting
        fields = '__all__'

    def create(self, validated_data):
        return PostingSerializer.__create_or_update(validated_data)

    def update(self, instance, validated_data):
        return PostingSerializer.__create_or_update(validated_data, instance)

    @staticmethod
    def __create_or_update(data, instance=None):
        """
        Static method which allows for creation or update of a posting
        :param instance: This is a instance
        :param data: the validated data from the serializer
        :return: A posting object
        """
        locations = data.pop('locations', {})
        skills = data.pop('skills', [])
        interests = data.pop('interests', [])
        employees = data.pop('employees', [])


        if instance is not None:
            posting = Posting(id=instance.id, **data)
            posting.save(force_update=True)

        else:
            posting = Posting(**data)
            posting.save(force_insert=True)

        if locations:
            st.update_posting_locations(posting, locations)
        if skills:
            st.update_posting_skills(posting, skills)
        if interests:
            st.update_posting_interests(posting, interests)
        if employees:
            st.update_posting_employees(posting, employees)

        return posting



