from .models import Permissions,PermissionsGroup
from Objects.models import TypeTransaction 

def create_parameterized_tables(function):
    def wrapper(*args, **kwargs):
        if (TypeTransaction.objects.all().count()) != 7:
            TypeTransaction.objects.delete()
            TypeTransaction.objects.create(name="Create")
            TypeTransaction.objects.create(name="Delete")
            TypeTransaction.objects.create(name="Add")
            TypeTransaction.objects.create(name="Subtract")
            TypeTransaction.objects.create(name="Update")
            TypeTransaction.objects.create(name="Returning")
            TypeTransaction.objects.create(name="Borrowing")
        if (Permissions.objects.all().count()) != 7:
            Permissions.objects.all().delete()
            Permissions.objects.create(name="Create_Objects")
            Permissions.objects.create(name="Delete_Objects")
            Permissions.objects.create(name="Update_Objects")
            Permissions.objects.create(name="View_Objects")
            Permissions.objects.create(name="Update_Users")
            Permissions.objects.create(name="Update_Log")
            Permissions.objects.create(name="View_Log")
        if (PermissionsGroup.objects.all().count()) != 2:
            PermissionsGroup.objects.all().delete()
            teacher = PermissionsGroup.objects.create(name="Profesor")
            teacher.permissions_id.add(
                Permissions.objects.get(name="Create_Objects"),
                Permissions.objects.get(name="Delete_Objects"),
                Permissions.objects.get(name="Update_Objects"),
                Permissions.objects.get(name='View_Objects'),
                Permissions.objects.get(name="Update_Log"),
                Permissions.objects.get(name="View_Log")
                )
            student = PermissionsGroup.objects.create(name="Estudiante")
            student.permissions_id.add(
                Permissions.objects.get(name='View_Objects'),
                Permissions.objects.get(name="View_Log") 
                )
        return function(*args, **kwargs)
    return wrapper
    