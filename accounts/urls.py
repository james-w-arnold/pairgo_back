from django.conf.urls import url, include
from .views import LoginView, UserRegistrationView, CreateCandidateView, UserTypeView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'candidates', CreateCandidateView, base_name='candidate')
router.register(r'user_type', UserTypeView, base_name='user_type')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^register$', UserRegistrationView.as_view(), name='register')

]