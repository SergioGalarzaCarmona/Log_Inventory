from django.contrib import admin
from .models import Object, ObjectsGroup, TypeTransaction, Transaction

# Register your models here.
admin.site.register(Object)
admin.site.register(ObjectsGroup)
admin.site.register(TypeTransaction)
admin.site.register(Transaction)