from django.db import models
from Objects.models import Objects
from Users.models import Subprofile

# Create your models here.
class Borrowings(models.Model):
    object = models.ForeignKey(
        Objects,
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
