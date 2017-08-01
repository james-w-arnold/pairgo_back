from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as lazy
from accounts.models import User, CandidateLocation, CandidateSkill, CandidatePsychometrics, CandidateEducation, CandidateInterest, Candidate
from commons.models.commons import Location, Skill, Interest
import accounts.tools.serializer_tools as st
from django.core.exceptions import ValidationError
import logging

from rest_framework import serializers

class CustomAuthTokenSerializer(serializers.Serializer):
    """
    A custom serializer to handle the transfer of the AuthToken data over the api
    """
    email = serializers.EmailField(label=lazy("Email"))
    password = serializers.CharField(label=lazy("Password"),
                                     style={'input_type' : 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:

                if not user.is_active:
                    msg = lazy("This account has been disabled")
                    raise serializers.ValidationError(msg, code='authorization')

            else:
                msg = lazy("Unable to log in with the provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")

        else:
            msg = lazy('Cannot authorize with "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer to control the creation of new accounts within the system
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password' : {'write_only': True}
        }

    def create(self, validated_data):
        data = validated_data
        user = User(
            email=data['email'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        user.set_password(data['password'])
        user.save()
        return user


class LocationSerializer(serializers.ModelSerializer):
    """
    Serialization of the location model
    """
    class Meta:
        model = Location
        exclude = ('id',)

    def to_representation(self, instance):
        if instance:
            return {"name": instance.title, "geo": {"lat": instance.lat, "lon": instance.lon}}
        return {}

class CandidateLocationSerializer(serializers.Serializer):
    def to_representation(self, obj):
        locations = CandidateLocation.objects.filter(candidate__id=obj.instance.id)
        #divide the locations into two categories, the current location and the desired/potential locations
        current = {}
        potential = []
        if locations.exists():
            for location in locations:
                if location.current:
                    current = (LocationSerializer(location.location)).data
                else:
                    serializedLocation = (LocationSerializer(location.location)).data
                    potential.append(serializedLocation)

        return {'current': current, 'potential': potential}

    def to_internal_value(self, data):
        current_location = data.get('current', {})
        potential_locations = data.get('potential', [])

        current = {}
        potential = []

        if current_location:
            current = CandidateLocationSerializer.__parse_location(current_location)

        if potential_locations:
            for location in potential_locations:
                potential.append(CandidateLocationSerializer.__parse_location(location))

        return {"current": current, "potential": potential}


    @staticmethod
    def __parse_location(location):

        data = {"title": location.get('title', ''),
                'lat': location.get('lat'),
                'lon': location.get('lon')}
        serializer = LocationSerializer(data=data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            return validated_data

        else:
            return ValidationError('Incorrect Location Data')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        exclude = ('id', 'category')

class CandidateSkillSerializer(serializers.Serializer):
    def to_representation(self, object):
        skills = CandidateSkill.objects.filter(candidate__id=object.instance.id)

        return {"skills" : skills}

    def to_internal_value(self, data):

        return {"skills" : data}


class PsychometricSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidatePsychometrics
        exclude = ('id', 'user')

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        exclude = ('id',)

class CandidateInterestSerializer(serializers.Serializer):
    def to_representation(self, obj):
        candidate_interests = CandidateInterest.objects.filter(candidate__id=obj.instance.id)
        _interests = []

        if candidate_interests.exists():
            for item in candidate_interests:
                _interests.append(item)

        return {"interests" : _interests}

    def to_internal_value(self, data):
        interest_data = data
        _interests = []

        if interest_data:
            for item in interest_data:
                _interests.append(item)

        return {"interests" : _interests}

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateEducation
        exclude = ('id', 'user')

class CandidateSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name  = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')
    locations = CandidateLocationSerializer(required=True)
    educations = EducationSerializer(many=True, required=True)
    skills = CandidateSkillSerializer()
    interests = CandidateInterestSerializer()
    psychometrics = PsychometricSerializer()

    class Meta:
        model = Candidate
        fields = '__all__'

    def create(self, validated_data):
        logger = logging.getLogger(__name__)
        logger.error(validated_data)
        return CandidateSerializer.__update_or_create(validated_data)



    def update(self, validated_data, instance):
        return CandidateSerializer.__update_or_create(validated_data, instance)

    @staticmethod
    def __update_or_create(self, validated_data, instance=None):
        """
        Private method to override the default creation methods in the default update and create methods
        """
        _locations = validated_data.pop('locations', {'current': {}, 'potential': []})
        _skills = validated_data.pop({'skills' : []})
        _interests = validated_data.pop({'interests': []})
        _psychometrics = validated_data.pop({'psychometric_analysis': {}})
        _educations = validated_data.pop('educations', {})

        if instance is not None:
            #updated an existing candidate
            candidate = Candidate(id=instance.id, **validated_data)
            candidate.save(force_update=True)
        else:
            #or create a new candidate
            candidate = Candidate(**validated_data)
            candidate.save(force_insert=True)

        st.update_locations(_locations, candidate)
        st.update_skills(_skills, candidate)
        st.update_interests(_interests, candidate)
        st.update_psychometrics(_psychometrics, candidate)

        if _educations:
            st.update_educations(_educations, candidate)
        return candidate

