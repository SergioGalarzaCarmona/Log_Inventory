from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password

# Create your models here.

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
    permissions_id = models.ForeignKey (
        Permissions, 
        on_delete=models.CASCADE
        )
    
    class Meta:
        verbose_name = 'GroupPermission'
        verbose_name_plural = 'GroupPermissions'
        indexes = [
            models.Index(fields=['id', 'permissions_id'], name='permissions_group_idx'),
        ]

class Profile(models.Model):
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
        
class SubprofilesGroup(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=100)
    image = models.ImageField(
        default='default_group.jpg',
        upload_to='profile_images')
    permissions = models.ForeignKey(
        PermissionsGroup, 
        on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'GroupSubprofile'
        verbose_name_plural = 'GroupSubprofiles'
        
class Subprofile(models.Model):
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
        
    def authenticate(username,password):
        subuser = Subprofile.objects.filter(username=username)
        if len(subuser) > 1:
            raise ValueError('There are more than one user with the same username')
        password_verified = check_password(password,subuser[0].password)
        print(password_verified)
        if password_verified == True:
            return subuser
        else:
            return None
        
    