from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserSession, Profile
from django.contrib.auth.models import User

@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    session_key = request.session.session_key
    UserSession.objects.update_or_create(
        user=user,
        defaults={"session_key": session_key}
    )
