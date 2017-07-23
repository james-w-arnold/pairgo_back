from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as lazy
from accounts.models import User, CandidateLocation, CandidateSkill, CandidatePsychometrics, CandidateEducation
from commons.models.commons import Location, Skill

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
        potential_locations = data.get('desired', [])

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
        geo = location.get('geo', {})
        data = {"title": location.get('ti   tle', ''),
                'lat': geo.get('lat'),
                'lon': geo.get('lon')}
        serializer = LocationSerializer(data=data)

        if serializer.is_valid():
            validated_data = serializer.validated_data

        return validated_data


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        exclude = ('id', 'category')

class CandidateSkillSerializer(serializers.Serializer):
    def to_representation(self, instance):
        candidate_skills = CandidateSkill.objects.filter(candidate__id=obj.instance.id)

        return {'skills': candidate_skills}

class PsychometricSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidatePsychometrics
        exclude = ('id',)

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateEducation
        exclude = ('id',)

class CandidateSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name  = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')
    locations = CandidateLocationSerializer(required=True)
    educations = EducationSerializer(many=True, required=True)
    skills = CandidateSkillSerializer()
    psychometrics =