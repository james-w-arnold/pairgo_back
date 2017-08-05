from commons.models.commons import Interest, Industry
from employers.models import EmployerInterest, CompanyIndustry

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


        if interest_to_add:
            for interest in interest_to_add:
                EmployerInterest.objects.create(employer=instance,
                                                interest=interest)


def update_industries(instance, industries):
    """
    Helper function which creates/updates the industries of a company. it ensures there is no redundancy of industries
    """
    company_industries_all = CompanyIndustry.objects.filter(company=instance)
    company_industries = set(company_industries_all)
    received_industries = industries

    if received_industries:

        received_industries_set = set()

        for industry in received_industries:
            industry_to_add, nada = Industry.objects.get_or_create(name=industry.name,
                                                                   category=industry.category)
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
