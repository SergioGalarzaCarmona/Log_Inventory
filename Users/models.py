from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Permissions(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.name} Permission'
    
    class Meta:
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'


class PermissionsGroup(models.Model):
    permissions_id = models.ForeignKey(Permissions, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.name} Group Permission'
    
    class Meta:
        verbose_name = 'GroupPermission'
        verbose_name_plural = 'GroupPermissions'
        indexes = [
            models.Index(fields=['id', 'permissions_id'], name='permissions_group_idx'),
        ]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_images')
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        
class Subprofile(models.Model):
    profile_id = models.ForeignKey(Profile,on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg',upload_to='profile_images')
    
    def __str__(self):
        return f'{self.user.username} Subprofile'
    
    class Meta:
        verbose_name = 'Subprofile'
        verbose_name_plural = 'Subprofiles'
        
        indexes = [
            models.Index(fields=['profile_id', 'username'],name= 'profile_subprofile_idx'),
        ]


class SubprofilesGroup(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subprofile_id = models.ForeignKey(Subprofile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default_group.jpg',upload_to='profile_images')
    permissions = models.ForeignKey(PermissionsGroup, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.name} Group'
    
    class Meta:
        verbose_name = 'GroupSubprofile'
        verbose_name_plural = 'GroupSubprofiles'
        indexes = [
            models.Index(fields=['id', 'subprofile_id'], name='subprofile_group_idx'),
        ]
        

    