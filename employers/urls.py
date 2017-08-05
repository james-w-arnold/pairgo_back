from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from employers.views import EmployerLeadView, CompanyView

router = DefaultRouter()
router.register(r'employer_lead', EmployerLeadView, base_name='employer_lead')
router.register(r'company', CompanyView, base_name='company')

urlpatterns = [
    url(r'^', include(router.urls)),
]