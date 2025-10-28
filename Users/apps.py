from django.apps import AppConfig
from django.core.validators import RegexValidator


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Users"

    def ready(self):
        import Users.signals
        super().ready()
        
        from django.contrib.auth.models import User
        from .forms import CustomUsernameValidator
        
        User.username_validator = CustomUsernameValidator()

        # Mantener los validadores existentes (longitud, null, etc.)
        field = User._meta.get_field('username')
        field.validators = [
            v for v in field.validators if not isinstance(v, RegexValidator)
        ]
        field.validators.append(User.username_validator)

