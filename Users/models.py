from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_images')
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        
    
class GroupSubprofiles(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default_group.jpg',upload_to='profile_images')
    
    def __str__(self):
        return f'{self.name} Group'
    
    class Meta:
        verbose_name = 'GroupSubprofile'
        verbose_name_plural = 'GroupSubprofiles'
        
class Subprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg',upload_to='profile_images')
    
    def __str__(self):
        return f'{self.user.username} Subprofile'
    
    class Meta:
        verbose_name = 'Subprofile'
        verbose_name_plural = 'Subprofiles'
    