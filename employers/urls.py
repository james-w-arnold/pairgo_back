from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from employers.views import EmployerLeadView, CompanyView, EmployeeView, ListTeamMembers, TeamView

router = DefaultRouter()
router.register(r'employer_lead', EmployerLeadView, base_name='employer_lead')
router.register(r'company', CompanyView, base_name='company')
router.register(r'employee', EmployeeView, base_name='employee')
router.register(r'teams', TeamView, base_name='teams')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^teammembers/(?P<team>[\w-]+)/$', ListTeamMembers.as_view(), name='list_teammembers'),
]