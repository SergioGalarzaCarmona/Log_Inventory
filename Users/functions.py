from .models import Permissions,PermissionsGroup, TypeChanges
from Objects.models import TypeTransaction
from django.utils.translation import gettext as _
import functools
from asgiref.sync import iscoroutinefunction, sync_to_async

def create_parameterized_tables(function):

    async def async_setup():
        # Wrap the existing ORM logic inside sync_to_async to avoid blocking
        await sync_to_async(_setup_tables)()

    def sync_setup():
        _setup_tables()

    @functools.wraps(function)
    async def async_wrapper(*args, **kwargs):
        await async_setup()
        return await function(*args, **kwargs)

    @functools.wraps(function)
    def sync_wrapper(*args, **kwargs):
        sync_setup()
        return function(*args, **kwargs)

    if iscoroutinefunction(function):
        return async_wrapper
    return sync_wrapper

def _setup_tables():
    """This contains your original ORM setup code."""
    if TypeTransaction.objects.count() != 6:
        TypeTransaction.objects.all().delete()
        TypeTransaction.objects.create(name="Create")
        TypeTransaction.objects.create(name="Delete")
        TypeTransaction.objects.create(name="Add")
        TypeTransaction.objects.create(name="Subtract")
        TypeTransaction.objects.create(name="Update")
        TypeTransaction.objects.create(name="Returning")

    if Permissions.objects.count() != 8:
        Permissions.objects.all().delete()
        Permissions.objects.create(name="Create_Objects")
        Permissions.objects.create(name="Delete_Objects")
        Permissions.objects.create(name="Update_Objects")
        Permissions.objects.create(name="View_Objects")
        Permissions.objects.create(name="Update_Users")
        Permissions.objects.create(name="Update_Log")
        Permissions.objects.create(name="View_Objects_Log")
        Permissions.objects.create(name="View_Users_Log")

    if PermissionsGroup.objects.count() != 2:
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

    if TypeChanges.objects.count() != 3:
        TypeChanges.objects.all().delete()
        TypeChanges.objects.create(value="Create")
        TypeChanges.objects.create(value="Update")
        TypeChanges.objects.create(value="Delete")
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

def get_description(description : str):
    description = description.split('\n')
    description = [i.split(' ') for i in description]
    for i in description:
        subdescription = [t.replace(',','') for t in i]
        description.append(subdescription)
    return description

