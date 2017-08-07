from commons.models.commons import Interest, Industry
from employers.models import EmployerInterest, CompanyIndustry, EmployeeInterest, TeamMember, Team, EmployeePsychometrics
import logging

def update_interests(instance, interests):
    """
    used to update the interests associated with an employer
    :param instance: a User instance provided by request
    :param interests: a array of interests
    :return: void
    """

    received_interests = interests

    if received_interests:
        employer_interests_all = EmployerInterest.objects.filter(employer=instance)
        employer_interests = set(employer_interests_all)

        received_interests_set = set()

        for interest in received_interests:
            interest_to_add, nada = Interest.objects.get_or_create(name=interest)
            received_interests_set.add(interest_to_add)

        interests_to_add = received_interests_set - employer_interests
        interests_to_delete = employer_interests - received_interests_set

        if interests_to_delete:
            for interest in interests_to_delete:
                employer_interests_all.filter(interest__name=interest.interest.name).delete()


        if interests_to_add:
            for interest in interests_to_add:
                EmployerInterest.objects.create(employer=instance,
                                                interest=interest)


def update_industries(instance, industries):
    """
    Helper function which creates/updates the industries of a company. it ensures there is no redundancy of industries
    """
    company_industries_all = CompanyIndustry.objects.filter(company=instance)
    company_industries = set(company_industries_all)
    received_industries = industries

    logger = logging.getLogger(__name__)
    logger.error(industries)

    if received_industries:

        received_industries_set = set()

        for industry in received_industries:
            industry_to_add, nada = Industry.objects.get_or_create(name=industry['name'],
                                                                   category=industry['category'])
            received_industries_set.add(industry_to_add)

        industries_to_add = received_industries_set - company_industries
        industries_to_delete = company_industries - received_industries_set

        if industries_to_delete:
            for industry in industries_to_delete:
                company_industries_all.filter\
                    (company=instance,
                     industry=industry).delete()

        if industry_to_add:
            for industry in industries_to_add:
                CompanyIndustry.objects.create(
                    company=instance,
                    industry=industry
                )


def update_employee_interests(instance, interests):
    """
    helper function to update the interests of an employee
    :param instance: the employee object which is to be updated
    :param interests: a list of interests
    :return: void
    """
    employee_interests_all = EmployeeInterest.objects.filter(employee=instance)
    employee_interests = set(employee_interests_all)
    if interests:
        received_interests_set = set()

        for interest in interests:
            interest_to_add, nada = Interest.objects.get_or_create(
                name=interest
            )
            received_interests_set.add(interest_to_add)

        interests_to_add = received_interests_set - employee_interests
        interests_to_delete = employee_interests - received_interests_set

        if interests_to_delete:
            for interest in interests_to_delete:
                employee_interests_all.filter(
                    interest=interest,
                    employer=instance
                ).delete()

        if interest_to_add:
            for interest in interests_to_add:
                EmployeeInterest.objects.create(
                    employee=instance,
                    interest=interest
                )


def update_team_members(instance, teams):
    team_members_all = TeamMember.objects.filter(employee=instance)
    team_members = set(team_members_all)

    if teams:
        received_teams = set()
        for team in teams:
            team_to_add = Team.objects.get(
                team_name=team['team_name'],
                company__company_name=team['company']
            )
            received_teams.add(team_to_add)

        teams_to_add = received_teams - team_members
        teams_to_delete = team_members - received_teams

        if teams_to_delete:
            for team in teams_to_delete:
                team_members_all.filter(
                    team__team_name=teams['team_name'],
                    team__company__company_name=teams['company']
                ).delete()

        if teams_to_add:
            for team in teams_to_add:
                TeamMember.objects.create(
                    employee=instance,
                    team=team
                )


def update_employee_psychometrics(instance, psychometric):
    """
    helper method to add or update any psychometrics onto an employee
    :param instance: an employee object
    :param psychometric: the psychometric values
    :return: void
    """

    if psychometric:
        #get existing model or create
        logger = logging.getLogger(__name__)
        logger.error(psychometric)
        logger.error(instance.id)
        employee_psychometrics = EmployeePsychometrics.objects.update_or_create(
            employee=instance,
            **psychometric
        )
        #employee_psychometrics.extroversion = psychometric['extroversion']
        #employee_psychometrics.neuroticism = psychometric['neuroticism']
        #employee_psychometrics.openness_to_experience = psychometric['openness_to_experience']
        #employee_psychometrics.conscienciousness = psychometric['conscienciousness']
        #employee_psychometrics.agreeableness = psychometric['agreeableness']

        #employee_psychometrics.save()

