from django.db import models
from django.contrib.auth.models import User
from Users.models import Subprofile

# Create your models here.
class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default_group.jpg',upload_to='media/objects_images')
    in_charge = models.ForeignKey(Subprofile, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.name} Object Group '
    
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

class Object(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg',upload_to='media/objects_images')
    description = models.TextField()
    stock = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    in_charge = models.ForeignKey(Subprofile, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.name} Object'
    
    class Meta:
        verbose_name = 'Object'
        verbose_name_plural = 'Objects'
        
class TypeTransaction(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.name} Transaction Type'
    
    class Meta:
        verbose_name = 'TypeTransaction'
        verbose_name_plural = 'TypeTransactions'

class Transaction(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    type = models.ForeignKey(TypeTransaction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    in_charge = models.ForeignKey(Subprofile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    stock_before = models.IntegerField()
    stock_after = models.IntegerField()
    
    def __str__(self):
        return f'{self.object.name} Transaction'
    
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'