from django.contrib import admin
from .models import Object, ObjectsGroup, TypeTransaction, Transaction

# Register your models here.
admin.register(Object)
admin.register(ObjectsGroup)
admin.register(TypeTransaction)
admin.register(Transaction)