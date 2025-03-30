from .models import Permissions,PermissionsGroup, TypeChanges
from Objects.models import TypeTransaction
from django.utils.translation import gettext as _

def create_parameterized_tables(function):
    def wrapper(*args, **kwargs):
        if (TypeTransaction.objects.all().count()) != 6:
            TypeTransaction.objects.all().delete()
            TypeTransaction.objects.create(name="Create")
            TypeTransaction.objects.create(name="Delete")
            TypeTransaction.objects.create(name="Add")
            TypeTransaction.objects.create(name="Subtract")
            TypeTransaction.objects.create(name="Update")
            TypeTransaction.objects.create(name="Returning")
        if (Permissions.objects.all().count()) != 8:
            Permissions.objects.all().delete()
            Permissions.objects.create(name="Create_Objects")
            Permissions.objects.create(name="Delete_Objects")
            Permissions.objects.create(name="Update_Objects")
            Permissions.objects.create(name="View_Objects")
            Permissions.objects.create(name="Update_Users")
            Permissions.objects.create(name="Update_Log")
            Permissions.objects.create(name="View_Objects_Log")
            Permissions.objects.create(name="View_Users_Log")
        if (PermissionsGroup.objects.all().count()) != 2:
            PermissionsGroup.objects.all().delete()
            teacher = PermissionsGroup.objects.create(name="Profesor")
            teacher.permissions_id.add(
                Permissions.objects.get(name="Create_Objects"),
                Permissions.objects.get(name="Delete_Objects"),
                Permissions.objects.get(name="Update_Objects"),
                Permissions.objects.get(name='View_Objects'),
                Permissions.objects.get(name="Update_Log"),
                Permissions.objects.get(name="View_Objects_Log"),
                Permissions.objects.get(name="View_Users_Log")
                )
            student = PermissionsGroup.objects.create(name="Estudiante")
            student.permissions_id.add(
                Permissions.objects.get(name='View_Objects'),
                Permissions.objects.get(name="View_Objects_Log") 
                )
        if (TypeChanges.objects.all().count()) != 3:
            TypeChanges.objects.all().delete()
            TypeChanges.objects.create(value="Create")
            TypeChanges.objects.create(value="Update")
            TypeChanges.objects.create(value="Delete")
        return function(*args, **kwargs)
    return wrapper


def create_description(object : object,type : str,**kwargs):
    if type == 'Subuser':
        initial =  {
            'username' : object.username,
            'email' : object.email,
            'group' : object.subprofile.group.name,
        }
    if type == 'SubuserGroup':
        initial = {
            'name' : object.name,
            'permissions' : str(object.permissions.pk)
        }
    return '\n'.join([f'Change in {key}, before: {initial[key]}, after: {kwargs[key]}' for key in kwargs.keys() if initial[key] != kwargs[key]])

    