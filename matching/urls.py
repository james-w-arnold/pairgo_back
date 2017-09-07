from django.conf.urls import url

from .views import CandidateGetMatchView, EmployerGetMatchView
urlpatterns = [
    url(r'^matches/candidate/(?P<candidate>[\w-]+$)', CandidateGetMatchView.as_view(), name='candidate_get_match'),
    url(r'^matches/employer/(?P<employer>[\w-]+$)', EmployerGetMatchView.as_view(), name='employer_get_match'),

]