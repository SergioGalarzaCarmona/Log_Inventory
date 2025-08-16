from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import UserSession

class OneSessionPerUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                user_session = UserSession.objects.get(user=request.user)
                if user_session.session_key != request.session.session_key:
                    logout(request)
                    messages.error(request, "Tu sesión ha sido cerrada porque tu cuenta inició en otro dispositivo.")
                    return redirect('/authenticate_user/deactivate') 
            except UserSession.DoesNotExist:
                pass

        return self.get_response(request)