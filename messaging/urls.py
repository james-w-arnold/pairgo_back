from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import ThreadView

router = DefaultRouter()
router.register(r'thread', ThreadView, base_name='thread view')
urlpatterns = [
    url(r'^', include(router.urls)),
]