from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import (
    Objects,
    ObjectsGroup,
    Transaction,
    GroupObjectsChanges,
    TypeChanges,
    TypeTransaction,
)
from .functions import create_transaction_description
from Users.middleware import get_current_user


@receiver(pre_save, sender=Objects)
def before_save_object(sender, instance, **kwargs):
    if instance.pk:
        instance._old_instance = sender.objects.get(pk=instance.pk)


@receiver(post_save, sender=Objects)
def after_saving_object(sender, instance, created, **kwargs):

    user = get_current_user()

    if created:
        description = (
            f"Se creó el objeto {instance.name} con stock inicial de {instance.stock}."
        )
        type_transaction = TypeTransaction.objects.get(name="Create")
        stock_before = 0
        stock_after = instance.stock

    if hasattr(instance, "_old_instance"):
        if not instance.is_active:
            description = f"Se eliminó el objeto {instance.name} que tenía un stock de {instance.stock}."
            type_transaction = TypeTransaction.objects.get(name="Delete")
            stock_before = instance.stock
            stock_after = 0

        else:
            try:
                description = create_transaction_description(instance, "Object")
                type_transaction = TypeTransaction.objects.get(name="Update")
                stock_before = instance._old_instance.stock
                stock_after = instance.stock
            except sender.DoesNotExist:
                pass

    if description:
        Transaction.objects.create(
            user=instance.user,
            type=type_transaction,
            object=instance,
            in_charge=user,
            stock_before=stock_before,
            stock_after=stock_after,
            description=description,
        )


@receiver(pre_save, sender=ObjectsGroup)
def before_saving_object_group(sender, instance, **kwargs):
    if instance.pk:
        instance._old_instance = sender.objects.get(pk = instance.pk)

@receiver(post_save, sender=ObjectsGroup)
def after_saving_object_group(sender, instance, created, **kwargs):
    
    user = get_current_user()
    
    if created:
        description = (
            f"Se creó el grupo de objetos {instance.name}."
        )
        type_change = TypeChanges.objects.get(value="Create")
        
        
    if hasattr(instance, "_old_instance"):
        
        if not instance.is_active:
            
            description = f"Se eliminó el grupo de objetos {instance.name}."
            type_change = TypeChanges.objects.get(value="Delete")

        else:
            try:
                
                description = create_transaction_description(instance, 'ObjectGroup')
                type_change = TypeChanges.objects.get(value="Update")
                
            except sender.DoesNotExist:
                pass
    if description:
    	GroupObjectsChanges.objects.create(
    	    main_user=instance.user,
    	    group_changed=instance,
    	    user=user,
    	    type_change=type_change,
    	    description=description,
    	    )
