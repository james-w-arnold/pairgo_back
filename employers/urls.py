from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from employers.views import EmployerLeadView, CompanyView, EmployeeView, ListTeamMembers, TeamView, InviteEmployee, EmployerLeadPsychoViewset, EmployeePsychometricsView, GetTeamByCompanyView

router = DefaultRouter()
router.register(r'employer_lead', EmployerLeadView, base_name='employer_lead')
router.register(r'company', CompanyView, base_name='company')
router.register(r'employee', EmployeeView, base_name='employee')
router.register(r'employee_psychometrics', EmployeePsychometricsView, base_name='employee psychometrics')
router.register(r'teams', TeamView, base_name='teams')
router.register(r'invite', InviteEmployee, base_name='invite employees')
router.register(r'employer_psychometrics', EmployerLeadPsychoViewset, base_name='Employer lead psychometrics')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^teammembers/(?P<team>[\w-]+)/$', ListTeamMembers.as_view(), name='list_teammembers'),
    url(r'^invite', InviteEmployee.as_view()),
    url(r'^company_team_lookup/(?P<company>[\w-]+)$', GetTeamByCompanyView.as_view(), name='get_team_by_company'),

]