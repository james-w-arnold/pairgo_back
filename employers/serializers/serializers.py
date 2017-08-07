from rest_framework import serializers
from employers import models
from employers.utils import serializer_tools as st
import logging

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        exclude = ('id',)

class EmployerPsychometricSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmployerPsychometrics
        exclude = ('id', 'employer')


class EmployerInterestSerializer(serializers.Serializer):
    def to_representation(self, instance):
        employer_interests = models.EmployerInterest.objects.filter(employer__id=instance.instance.id)

        interests = [interest.interest.name for interest in employer_interests]
        return interests
    def to_internal_value(self, data):
        interests = []

        for interest in data:
            interests.append(interest)

        return interests

class EmployerSerializer(serializers.ModelSerializer):

    first_name = serializers.SerializerMethodField()
    last_name  = serializers.SerializerMethodField()
    email      = serializers.SerializerMethodField()

    interests = EmployerInterestSerializer(required=False)
    #team = TeamSerializer(required=False)
    psychometrics = EmployerPsychometricSerializer(required=False)


    class Meta:
        model = models.Employer
        fields = '__all__'
        read_only_fields = ('first_name', 'last_name', 'email')

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_email(self, obj):
        return obj.user.email

    def create(self, validated_data):
        company = validated_data.get('company', None)
        team = validated_data.pop('team', None)
        psychometrics = validated_data.pop('psychometrics', None)
        interests = validated_data.pop('interests', None)
        employer = models.Employer(**validated_data)
        logger = logging.getLogger(__name__)
        logger.error(interests)
        employer.save(force_insert=True)

        if company:
            comp, nada = models.Company.objects.get_or_create(id=company)
            employer.company = comp


        if team:
            curr_team = models.Team.objects.get(team_name=team['name'], company=company)
            if curr_team.exists():
                employer.team = curr_team

            else:
                new_team = TeamSerializer(**team).create()
                employer.team = new_team


        if psychometrics:
            psycho = EmployerPsychometricSerializer(**psychometrics, employer=employer).create()

        if interests:
            st.update_interests(employer, interests)



        return employer

    def update(self, instance, validated_data):
        company = validated_data.pop('company', {})
        team = validated_data.pop('team', {})
        psychometrics = validated_data.pop('psychometrics', {})
        interests = validated_data.pop('interests', [])
        if company:
            comp, nada = models.Company.objects.get_or_create(id=company)
            instance.company = comp
            instance.save()
            #@todo: if company doesn't exist, create one. Need to implement company serializer first

        if team:
            curr_team = models.Team.objects.get(team_name=team['name'], company=company)
            if curr_team.exists():
                instance.team = curr_team

            else:
                new_team = TeamSerializer(**team).create()
                instance.team = new_team
                instance.save()

        if psychometrics:
            curr_psycho = models.EmployerPsychometrics.objects.get(employer=instance)
            if curr_psycho.exists():
                curr_psycho.delete()
            psycho = EmployerPsychometricSerializer(**psychometrics, employer=instance).create()

        if interests:
            st.update_interests(instance, interests)

#---------------------------------------------COMPANY--------------------------------#

class CompanyIndustrySerializer(serializers.Serializer):
    def to_representation(self, instance):
        logger = logging.getLogger(__name__)
        logger.error(instance)
        industries = set(models.CompanyIndustry.objects.filter(company=instance.instance.id))

        industry_dict = [{'name' : ind.industry.name, 'category' : ind.industry.category} for ind in industries]

        return industry_dict

    def to_internal_value(self, data):
        industries = []
        for industry in data:
            industries.append(industry)
        return industries

class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer to create and update and get company models
    """

    industries = CompanyIndustrySerializer(required=True)

    class Meta:
        model = models.Company
        fields = '__all__'

    def create(self, validated_data):
        industries = validated_data.pop('industries', None)
        #@todo add employer serializer

        company = models.Company(**validated_data)
        company.save(force_insert=True)

        if industries is not None:
            st.update_industries(company, industries)

        return company

    def update(self, instance, validated_data):
        industries = validated_data.pop('industries', None)

        if industries is not None:
            st.update_industries(instance, industries)

        company = models.Company(id=instance.id, **validated_data)
        company.save(force_update=True)

        return company

