from django.urls import path
from .views import home, sign_up, main

urlpatterns = [
    path('home', home, name='home'),
    path('sign up', sign_up, name='sign_up'),
    path('work space', main, name='main'),
]