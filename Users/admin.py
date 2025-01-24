from django.contrib import admin
from .models import Profile, Subprofile, SubprofilesGroup, Permissions, PermissionsGroup

# Register your models here.
admin.site.register(Profile)
admin.site.register(Subprofile)
admin.site.register(SubprofilesGroup)
admin.site.register(Permissions)
admin.site.register(PermissionsGroup)