from django.urls import path
from Borrowings.views import manage_borrowings
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('borrowings/', manage_borrowings, name='manage_borrowings'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)