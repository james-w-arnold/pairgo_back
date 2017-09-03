from django.conf.urls import url, include
from .views import LoginView, UserRegistrationView, CreateCandidateView, UserTypeView, CandidatePsychometricsView, CandidateEducation
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'candidates', CreateCandidateView, base_name='candidate')
router.register(r'user_type', UserTypeView, base_name='user_type')
router.register(r'candidate/psychometrics', CandidatePsychometricsView, base_name='candidate_psychometrics')
router.register(r'candidate/education', CandidateEducation, base_name='candidate education')
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^register$', UserRegistrationView.as_view(), name='register'),
]