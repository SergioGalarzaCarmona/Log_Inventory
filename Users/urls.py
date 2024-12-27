from django.urls import path
from .views import home, start, main

urlpatterns = [
    path('home', home, name='home'),
    path('sign up', start, name='sign_up'),
    path('work space', main, name='main'),
]