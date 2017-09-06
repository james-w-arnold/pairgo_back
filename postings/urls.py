from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import PostingViewSet, RetrievePostingsView, TeamRetrievePostingsView

router = DefaultRouter()
router.register(r'postings', PostingViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^retrieve/(?P<employer>[\w-]+)$', RetrievePostingsView.as_view(), name='retrieve_posts'),
    url(r'^team_retrieve/(?P<team>[\w-]+)$', TeamRetrievePostingsView.as_view(), name='retrieve_posts_by_team')

]