def _setup_tables():

    from .models import Permissions, PermissionsGroup, TypeChanges
    from Objects.models import TypeTransaction

    # TYPE TRASACTION TABLE
    REQUIRED = ["Create", "Delete", "Add", "Substract", "Update"]
    for name in REQUIRED:
        TypeTransaction.objects.get_or_create(name=name)
    TypeTransaction.objects.exclude(name__in=REQUIRED).delete()

    # PERMISSIONS TABLE
    REQUIRED = [
        "Create_Objects",
        "Delete_Objects",
        "Update_Objects",
        "View_Objects",
        "Update_Users",
        "Update_Log",
        "View_Objects_Log",
        "View_Users_Log",
    ]
    for name in REQUIRED:
        Permissions.objects.get_or_create(name=name)
    Permissions.objects.exclude(name__in=REQUIRED).delete()

    # PERMISSIONS GROUP TABLE
    REQUIRED_GROUPS = ["Profesor", "Estudiante"]
    REQUIRED_TEACHER_PERMISSIONS = [
        "Create_Objects",
        "Delete_Objects",
        "Update_Objects",
        "View_Objects",
        "Update_Users",
        "Update_Log",
        "View_Objects_Log",
        "View_Users_Log",
    ]
    REQUIRED_STUDENT_PERMISSIONS = ["View_Objects", "View_Objects_Log"]

    for group_name in REQUIRED_GROUPS:
        group, created = PermissionsGroup.objects.get_or_create(name=group_name)

        if group_name == "Profesor":
            required = REQUIRED_TEACHER_PERMISSIONS
        else:
            required = REQUIRED_STUDENT_PERMISSIONS

        # Add required permissions
        for perm_name in required:
            perm, _ = Permissions.objects.get_or_create(name=perm_name)
            group.permissions_id.add(perm)

        # Remove extra permissions (only disassociate, not delete from DB)
        to_remove = group.permissions_id.exclude(name__in=required)
        group.permissions_id.remove(*to_remove)

    # TYPE CHANGES TABLE
    REQUIRED = ["Create", "Update", "Delete"]

    for value in REQUIRED:
        TypeChanges.objects.get_or_create(value=value)
    TypeChanges.objects.exclude(value__in=REQUIRED).delete()


def create_description(instance, model_type):
    if model_type == "Subuser":
        initial = {
            "nombres": instance._old_instance.first_name,
            "apellidos": instance._old_instance.last_name,
            "email": instance._old_instance.email,
            "grupo": str(instance._old_instance.subprofile.group),
        }
        
        updated  = {
            "nombres" : instance.first_name,
            "apellidos" : instance.last_name,
            "email" : instance.email,
            "grupo" : str(instance.subprofile.group),
        }
    if model_type == "SubuserGroup":
        initial = {
            "nombre": instance._old_instance.name,
            "descripción": instance._old_instance.description,
            "permisos": str(instance._old_instance.permissions),
        }

        updated = {
            "nombre": instance.name,
            "descripción": instance.description,
            "permisos": str(instance.permissions),
        }
        
    
    changes = [
        f"Cambio en {key}, antes: {initial[key]}, después: {updated[key]}"
        for key in initial.keys()
        if initial[key] != updated[key]
    ]
    
    return ", \n".join(changes) if changes else None


from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)

account_activation_token = AccountActivationTokenGenerator()
