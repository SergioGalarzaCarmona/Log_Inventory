from django.urls import path
from .views import main, log
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('work_space/', main, name='main'),
    path('log/',log, name='log'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)