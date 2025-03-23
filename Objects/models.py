from django.db import models
from django.contrib.auth.models import User
from Users.models import Subprofile

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

class ObjectsGroup(BaseAuditModel):
    name = models.CharField(
        max_length=100
        )
    image = models.ImageField(
        default='default_group.jpg',
        upload_to='objects_images'
        )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE)
    in_charge = models.ForeignKey(
        Subprofile, 
        on_delete=models.CASCADE
        )
    
    def __str__(self):
        return f'{self.name} Object Group '

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

class Object(BaseAuditModel):
    group = models.ForeignKey(
        ObjectsGroup,
        on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
        )
    name = models.CharField(
        max_length=100
        )
    stock = models.IntegerField()
    image = models.ImageField(
        default='default.jpg',
        upload_to='objects_images'
        )
    description = models.TextField()
    in_charge = models.ForeignKey(
        Subprofile, 
        on_delete=models.CASCADE
        )
    
    def __str__(self):
        return f'{self.name} Object'
    
    class Meta:
        verbose_name = 'Object'
        verbose_name_plural = 'Objects'
        
class TypeTransaction(models.Model):
    name = models.CharField(
        max_length=100
        )
    
    def __str__(self):
        return f'{self.name} Transaction Type'
    
    class Meta:
        verbose_name = 'TypeTransaction'
        verbose_name_plural = 'TypeTransactions'

class Transaction(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
        )
    type = models.ForeignKey(
        TypeTransaction, 
        on_delete=models.CASCADE
        )
    object = models.ForeignKey(
        Object, 
        on_delete=models.CASCADE
        )
    in_charge = models.ForeignKey(
        Subprofile,
        on_delete=models.CASCADE
        )
    stock_before = models.IntegerField()
    stock_after = models.IntegerField()
    description = models.TextField()
    date = models.DateTimeField(
        auto_now_add=True
        )
    
    def __str__(self):
        return f'{self.object.name} Transaction'
    
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

class Borrowings(models.Model):
    object = models.ForeignKey(
        Object,
        on_delete=models.CASCADE
    )
    in_charge = models.ForeignKey(
        Subprofile,
        on_delete=models.CASCADE
    )
    date_init = models.DateTimeField(
        auto_now_add=True
    )
    date_limit = models.DateTimeField()
    date_complete = models.DateTimeField()
    stock = models.IntegerField()
    
    def __str__(self):
        return f'{self.object.name} Borrowing'
    
    class Meta:
        verbose_name = 'Borrowing'
        verbose_name_plural = 'Borrowings'
