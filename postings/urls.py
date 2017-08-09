from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import PostingViewSet

router = DefaultRouter()
router.register(r'postings', PostingViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]