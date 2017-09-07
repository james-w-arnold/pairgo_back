from rest_framework import serializers
from employers import models
from employers.utils import serializer_tools as st
import logging

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = '__all__'

class EmployerPsychometricSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmployerPsychometrics
        exclude = ('id',)


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
        employer = models.Employer.objects.get(id=instance.id)

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
            logger = logging.getLogger(__name__)

            emp_psycho = models.EmployerPsychometrics.objects.update_or_create(employer=employer, **psychometrics)

            #curr_psycho = models.EmployerPsychometrics.objects.filter(employer=instance.id)

            logger.error(emp_psycho)
            #psycho = models.EmployerPsychometrics.objects.create(employer=employer, **psychometrics)
            #psycho.save()
            #psycho = EmployerPsychometricSerializer(**psychometrics, employer=instance.id).create()

        if interests:
            st.update_interests(instance, interests)
        employer.save(force_update=True)
        return employer

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

#-----------------------------------------------employee serializers---------------------------------------

class EmployeeInterestSerializer(serializers.Serializer):
    def to_representation(self, instance):
        employee_intersts = models.EmployeeInterest.objects.filter(employee__id=instance.instance.id)

        interests = [interest.interest.name for interest in employee_intersts]
        return interests
    def to_internal_value(self, data):
        interests = []

        for interest in data:
            interests.append(interest)

        return interests

class EmployeePsychometricSerializer(serializers.Serializer):
    """
    Serializer to convert psychometrics into a readable format
    """
    def to_representation(self, instance):
        psychometrics = models.EmployeePsychometrics.objects.get(employee_id=instance.instance.id)
        psycho_json = {
            "extroversion" : psychometrics.extroversion,
            "neuroticism" : psychometrics.neuroticism,
            "openness_to_experience" : psychometrics.openness_to_experience,
            "conscientiousness" : psychometrics.conscientiousness,
            "agreeableness" : psychometrics.agreeableness
        }
        return psycho_json
    def to_internal_value(self, data):
        psychometrics = {
            "extroversion" : data['extroversion'] or "",
            "neuroticism" : data['neuroticism'] or "",
            "openness_to_experience" : data['openness_to_experience'] or "",
            "conscientiousness" : data['conscienciousness'] or "",
            "agreeableness" : data['agreeableness'] or ""
        }
        return psychometrics

class EmployeePsychometricsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmployeePsychometrics
        exclude = ('id', 'employee')

class TeamMemberSerializer(serializers.Serializer):
    def to_representation(self, instance):
        employee_teams = models.TeamMember.objects.filter(employee_id=instance.instance.id)

        teams = [{"team_name" : team.team.team_name, "company" : team.company.company_name} for team in employee_teams]
        return teams

    def to_internal_value(self, data):
        teams = []
        for team in data:
            teams.append(data)
        return teams

class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer to produce a serializable format of the employee model along with its associated models
    """
    teams = TeamMemberSerializer(required=False)
    psychometrics = EmployeePsychometricsModelSerializer(required=False)
    interests = EmployeeInterestSerializer(required=False)

    class Meta:
        model = models.Employee
        fields = ('user', 'about', 'job_title', 'company', 'id', 'psychometrics', 'interests', 'teams')
        read_only_fields = ('id', )
    def create(self, validated_data):
        return EmployeeSerializer.__update_or_create(validated_data)

    def update(self, instance, validated_data):
        return EmployeeSerializer.__update_or_create(validated_data, instance)

    @staticmethod
    def __update_or_create(data, instance=None):
        """
        :param data: the validated data passed to the serializer
        :param instance: the employee instance, this is only passed if updating the model
        :return: a created or updated employee model
        """
        interests = data.pop('interests', [])
        teams = data.pop('teams', [])
        psychometrics = data.pop('psychometrics', [])

        if instance is not None:
            employee = models.Employee(id=instance.id, **data)
            employee.save(force_update=True)
        else:
            employee = models.Employee(**data)
            employee.save(force_insert=True)

        if interests:
            st.update_employee_interests(employee, interests)

        if teams:
            st.update_team_members(employee, teams)

        if psychometrics:
            st.update_employee_psychometrics(employee, psychometrics)

        return employee


class TeamMembersModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TeamMember
        fields = '__all__'