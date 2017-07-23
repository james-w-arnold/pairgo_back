from django.conf.urls import url, include
from .views import LoginView, UserRegistrationView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^register$', UserRegistrationView.as_view(), name='register'),

]