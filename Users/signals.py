from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import UserSession

@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    session_key = request.session.session_key
    UserSession.objects.update_or_create(
        user=user,
        defaults={"session_key": session_key}
    )
