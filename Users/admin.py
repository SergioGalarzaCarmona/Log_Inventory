from django.contrib import admin
from .models import Profile, Subprofile, SubprofilesGroup, Permissions, PermissionsGroup

# Register your models here.
admin.register(Profile)
admin.register(Subprofile)
admin.register(SubprofilesGroup)
admin.register(Permissions)
admin.register(PermissionsGroup)