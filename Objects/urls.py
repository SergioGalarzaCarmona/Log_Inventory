from django.urls import path
from .views import main, log, edit_object, object_groups
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('work_space/', main, name='main'),
    path('work_space/<int:id>', edit_object, name='edit_object' ),
    path('object_groups/', object_groups, name='object_groups' ),
    path('log/',log, name='log'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)