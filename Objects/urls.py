from django.urls import path
from .views import main, log, manage_object, manage_object_groups, delete
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("work_space/", main, name="main"),
    path("work_space/<int:id>", manage_object, name="edit_object"),
    path("object_groups/", manage_object_groups, name="object_groups"),
    path("log/", log, name="log"),
    path('delete/',delete, name="delete")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
