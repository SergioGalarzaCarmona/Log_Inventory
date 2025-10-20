from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import UserSession
from .functions import _setup_tables
from asgiref.sync import sync_to_async
import threading

_tables_ready = False


class OneSessionPerUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                user_session = UserSession.objects.get(user=request.user)
                if user_session.session_key != request.session.session_key:
                    logout(request)
                    messages.error(
                        request,
                        "Tu sesión ha sido cerrada porque tu cuenta inició en otro dispositivo.",
                    )
                    return redirect("/authenticate_user/deactivate")
            except UserSession.DoesNotExist:
                pass

        return self.get_response(request)


class SetParameterizedTablesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global _tables_ready
        if not _tables_ready:
            _setup_tables()
        response = self.get_response(request)
        _tables_ready = True
        return response

    async def __acall__(self, request):
        global _tables_ready
        if not _tables_ready:
            await sync_to_async(_setup_tables)()
        response = await self.get_response(request)
        _tables_ready = True
        return response


_user = threading.local()

class CurrentUserMiddleware:
    """Guarda el usuario actual en un hilo local para ser usado en señales."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user if request.user.is_authenticated else None
        response = self.get_response(request)
        _user.value = None  # limpia después de la respuesta
        return response

def get_current_user():
    """Permite obtener el usuario actual desde cualquier lugar."""
    return getattr(_user, "value", None)