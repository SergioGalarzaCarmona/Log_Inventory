from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BaseAuditModel(models.Model):
    created = models.DateTimeField(
        auto_now_add = True
    )
    last_updated = models.DateTimeField(
        auto_now = True
    )
    is_active = models.BooleanField(
        default=True
    )
    class Meta:
        abstract = True

class UserSession(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    session_key = models.CharField(
        max_length=40, 
        blank=True, 
        null=True
    )

class Permissions(models.Model):
    name = models.CharField( 
        max_length=100
        )
    
    def __str__(self):
        return f'{self.name} Permission'
    
    class Meta:
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'


class PermissionsGroup(models.Model):
    permissions_id = models.ManyToManyField (
        Permissions, 
        related_name='permissions'
        )
    name = models.CharField (
        max_length=50,
    )
    
    class Meta:
        verbose_name = 'GroupPermission'
        verbose_name_plural = 'GroupPermissions'

    def __str__(self):
        return f'{self.name}'
class Profile(BaseAuditModel):
    user = models.OneToOneField (
        User, 
        on_delete=models.CASCADE
        )
    image = models.ImageField (
        default='default.jpg',
        upload_to='profile_images'
        )
     
    def __str__(self):
        return f'{self.user.username} Profile'
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def have_profile(self,user):
        try:
            profile = self.objects.get(user=user)
        except:
            return None
        return True, profile
        
class SubprofilesGroup(BaseAuditModel):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=100)
    image = models.ImageField(
        default='default_group.jpg',
        upload_to='subprofiles_groups_images')
    description = models.CharField(
        max_length=1000,
        default=''
    )
    permissions = models.ForeignKey(
        PermissionsGroup, 
        on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'GroupSubprofile'
        verbose_name_plural = 'GroupSubprofiles'
        
class Subprofile(BaseAuditModel):
    user = models.OneToOneField( 
        User,
        on_delete=models.CASCADE
        )
    profile = models.ForeignKey (
        Profile, 
        on_delete=models.CASCADE
        )
    image = models.ImageField (
        default='default.jpg',
        upload_to='profile_images')
    group = models.ForeignKey (
        SubprofilesGroup, 
        on_delete=models.CASCADE
        )
    
    def __str__(self):
        return f'{self.user.username} Subprofile'
    
    class Meta:
        verbose_name = 'Subprofile'
        verbose_name_plural = 'Subprofiles'

class TypeChanges(models.Model):
    value = models.CharField(
        
    )

class UserChanges(models.Model):
    main_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='main_user'
    )
    user_changed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = 'user_changed'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = 'user'
    )
    type_change = models.ForeignKey(
        TypeChanges,
        on_delete=models.CASCADE
    )
    description = models.CharField(
        max_length=1000,
        default=''
    )
    date = models.DateTimeField(
        auto_now_add = True
    )
    
    def __str__(self):
        return f'{self.description}'

    class Meta:
        verbose_name = 'UserChange'
        verbose_name_plural = 'UserChanges'
class GroupChanges(models.Model):
    main_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='main_user_group'
    )
    group_changed = models.ForeignKey(
        SubprofilesGroup,
        on_delete=models.CASCADE,
        related_name = 'user_changed_group'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = 'user_group'
    )
    type_change = models.ForeignKey(
        TypeChanges,
        on_delete=models.CASCADE
    )
    description = models.CharField(
        max_length=1000,
        default=''
    )
    date = models.DateTimeField(
        auto_now_add = True
    )
    
    def __str__(self):
        return f'{self.description}'
    
    class Meta:
        verbose_name = 'GroupChange'
        verbose_name_plural = 'GroupChanges'