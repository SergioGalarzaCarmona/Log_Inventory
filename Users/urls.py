from django.urls import path
from .views import home, sign_up

urlpatterns = [
    path('', home, name='home'),
    path('sign up', sign_up, name='sign_up'),
]