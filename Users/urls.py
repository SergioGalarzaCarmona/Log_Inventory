from django.urls import path
from .views import home, start, main,Logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('sign up/', start, name='sign_up'),
    path('work space/', main, name='main'),
    path('logout/', Logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)