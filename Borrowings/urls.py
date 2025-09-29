from django.urls import path
from Borrowings.views import manage_borrowings

urlpatterns = [
    path('borrowings/', manage_borrowings, name='manage_borrowings'),
]