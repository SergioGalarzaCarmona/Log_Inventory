from django.contrib import admin
from .models import Objects, ObjectsGroup, TypeTransaction, Transaction

# Register your models here.
admin.site.register(Objects)
admin.site.register(ObjectsGroup)
admin.site.register(TypeTransaction)
admin.site.register(Transaction)