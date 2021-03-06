import copy
import logging
from accounts.models import *
from commons.models.commons import Location, Skill, Interest

def update_locations(locations, instance):
    def location_get_or_create(location):
        loc = copy.copy(location)
        loc.pop('distance', None)
        loc['title'] = loc.get('title', '')
        new_location, _ = Location.objects.get_or_create(**loc)
        return new_location

    candidate_locations_current = instance.locations.filter(candidatelocation__current=True)
    candidate_locations_potential = set(instance.locations.filter(candidatelocation__current=False))

    locations_current   = locations.get('current', {})
    locations_potential = locations.get('potential', [])

    if locations_current:
        if not candidate_locations_current.filter(
                lat=locations_current['lat'],
                lon=locations_current['lon']).exists():
            CandidateLocation.objects.filter(candidate__id=instance.id, current=True).delete()
            location = location_get_or_create(locations_current)
            CandidateLocation.objects.create(candidate=instance,
                                             location=location,
                                             current=True)

    if locations_potential:
        potential_instances = set()
        for l in locations_potential:
            potential_instances.add(location_get_or_create(l))

        potential_to_delete = candidate_locations_potential - potential_instances
        potential_to_add = potential_instances - candidate_locations_potential

        if potential_to_delete:
            CandidateLocation.objects.filter(candidate__id=instance.id,
                                             location__in=potential_to_delete,
                                             current=False).delete()

        if potential_to_add:
            for item in potential_to_add:
                CandidateLocation.objects.create(candidate=instance,
                                                 location=item,
                                                 current=False)


def update_skills(skills, instance):

    #@todo: add support for categories within skills - soft/hard etc
    #def parse_skills(skill_collection):
     #   skills = skill_collection.get('skills')
      #  skill_names = []
       # for item in skills:
        #    skill_names.append(item['title'])

        #return skill_names

    #skill_titles = parse_skills(skills)

    skills_to_add = skills

    if skills_to_add:

        #get the existing skills
        candidate_skills_all = CandidateSkill.objects.filter(candidate=instance)
        candidate_skills = set(candidate_skills_all)
        received_skills = set()


        for skill in skills:

            skill_to_add, nada = Skill.objects.get_or_create(name=skill)
            received_skills.add(skill_to_add)

        delete_skills = candidate_skills - received_skills
        add_skills = received_skills - candidate_skills

        if delete_skills:
            for skill in delete_skills:
                candidate_skills_all.filter(skill__name=skill.skill.name).delete()

        if add_skills:
            for skill in add_skills:
                CandidateSkill.objects.create(candidate=instance, skill=skill)



def update_interests(interests, instance):

    #def parse_interests(interest_list):
     #   _interests = interests.get('interests')
      #  interest_names = []
#
 #       for item in interest_list:
  #          interest_names.append(item['name'])
#
 #       return interest_names


    interest_titles = interests
    received_interests = interests

    if received_interests:

        candidate_interests_all = CandidateInterest.objects.filter(candidate=instance)
        candidate_interests = set(candidate_interests_all)

        received_interests_set = set()

        for interest in interest_titles:
            interest_to_add, nada = Interest.objects.get_or_create(name=interest)
            received_interests_set.add(interest_to_add)



        interests_to_add = received_interests_set - candidate_interests
        interests_to_delete = candidate_interests - received_interests_set

        if interests_to_delete:
            for interest in interests_to_delete:
                candidate_interests_all.filter(interest__name=interest.interest.name).delete()

        if interests_to_add:
            for interest in interests_to_add:
                CandidateInterest.objects.create(candidate=instance, interest=interest)


def update_psychometrics(psychometrics, instance):

    if psychometrics:
        CandidatePsychometrics.objects.create(
            extroversion=psychometrics['extroversion'],
            neuroticism=psychometrics['neuroticism'],
            openness=psychometrics['openness'],
            conscientiousness=psychometrics['conscientiousness'],
            agreeableness=psychometrics['agreeableness'],
            candidate=instance
        )


def update_educations(educations, instance):

    if instance is not None:
        CandidateEducation.objects.filter(user=instance).delete()

    for edu in educations:
        edu['user'] = instance
        CandidateEducation.objects.update_or_create(**edu)


def assign_usertype(usertype, instance):
    userType = UserType(user=instance)

    if usertype == 'candidate':
        userType.isCandidate = True
    if usertype == 'employer':
        userType.isEmployer = True

    userType.save()
