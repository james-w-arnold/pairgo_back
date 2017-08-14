from .models import *
from commons.models.commons import *
import logging
def update_posting_interests(instance, interests):
    """
    Update the interests of a posting instance
    :param instance: a posting instance
    :param interests: an array of interests that are to be added to the posting
    :return: void
    """

    if interests:
        posting_interests_all = PostingInterest.objects.filter(posting=instance)
        posting_interests = set(posting_interests_all)
        received_interests = set()

        for interest in interests:
            interest_to_add, nada = Interest.objects.get_or_create(name=interest)
            received_interests.add(interest_to_add)

        interests_to_delete = posting_interests - received_interests
        interests_to_add = received_interests - posting_interests

        if interests_to_delete:
            for interest in interests_to_delete:
                posting_interests_all.filter(interest__name=interest.interest.name).delete()

        if interests_to_add:
            for interest in interests_to_add:
                PostingInterest.objects.create(posting=instance, interest= interest)


def update_posting_skills(instance, skills):
    """
    Update the skills attributed to a post
    :param instance: the posting instance
    :param skills: an array of skills
    :return: void
    """
    if skills:
        posting_skills_all = PostingSkill.objects.filter(posting=instance)
        posting_skills = set(posting_skills_all)
        received_skills = set()

        for skill in skills:
            skill_to_add, nada = Skill.objects.get_or_create(name=skill)
            received_skills.add(skill_to_add)

        skills_to_add = received_skills - posting_skills
        skills_to_delete = posting_skills - received_skills

        if skills_to_delete:
            for skill in skills_to_delete:
                posting_skills_all.filter(skill__name=skill.skill.name).delete()

        if skills_to_add:
            for skill in skills_to_add:
                PostingSkill.objects.create(posting=instance, skill=skill)


def update_posting_locations(instance, locations):
    """
    Method for updating the locations listed by a posting
    :param instance: the posting instance
    :param locations: the list of locations the internship is available at (can be one)
    :return: void
    """
    posting_locations_all = PostingLocation.objects.filter(posting=instance)
    posting_locations = set(posting_locations_all)
    received_locations = set()

    logger = logging.getLogger(__name__)
    logger.error(locations)
    if locations:
        for location in locations:
            loc, nada = Location.objects.get_or_create(**location)
            received_locations.add(loc)

        locations_to_delete = posting_locations - received_locations
        locations_to_add = received_locations - posting_locations

        if locations_to_delete:
            for location in locations_to_delete:
                posting_locations_all.filter(location=location).delete()

        if locations_to_add:
            for location in locations_to_add:
                PostingLocation.objects.create(posting=instance, location=location)

def update_posting_employees(instance, employees):

    posting_employees_all = PostingEmployee.objects.filter(posting=instance)
    posting_employees = set(posting_employees_all)

    received_employees = set()

    if employees:
        for employee in employees:
            emp, nada = Employee.objects.get(employee)
            received_employees.add(emp)

        employees_to_delete = posting_employees - received_employees
        employees_to_add = received_employees - posting_employees

        if employees_to_delete:
            for employee in employees_to_delete:
                posting_employees_all.filter(employee=employee)

        if employees_to_add:
            for employee in employees_to_add:
                PostingEmployee.objects.create(posting=instance, employee= employee)
