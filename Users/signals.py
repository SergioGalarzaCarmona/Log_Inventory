from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import UserSession
from .models import User, SubprofilesGroup, TypeChanges, UserChanges, GroupChanges
from .functions import create_description
from Users.middleware import get_current_user



@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    session_key = request.session.session_key
    UserSession.objects.update_or_create(
        user=user, defaults={"session_key": session_key}
    )





@receiver(pre_save, sender=User)
def before_save_object(sender, instance, **kwargs):
    if hasattr(instance, 'subprofile'):
        instance._old_instance = sender.objects.get(pk=instance.pk)


@receiver(post_save, sender=User)
def after_saving_object(sender, instance, created, **kwargs):
    
    description = None
    user = get_current_user()

    if hasattr(instance, "_old_instance"):
        if not instance.is_active:
            
            description = f'Se eliminó el usuario "{instance.first_name} {instance.last_name}" perteneciente al grupo "{instance.subprofile.group.name}".'
            type_change = TypeChanges.objects.get(value="Delete")
            
        else:
            try:
                description = create_description(instance, "Subuser")
                type_change = TypeChanges.objects.get(value="Update")
                
            except sender.DoesNotExist:
                pass

    if description:
        UserChanges.objects.create(
                main_user=instance.subprofile.profile.user,
                user_changed=instance,
                user=user,
                description=description,
                type_change=type_change)


@receiver(pre_save, sender=SubprofilesGroup)
def before_saving_object_group(sender, instance, **kwargs):
    if instance.pk:
        instance._old_instance = sender.objects.get(pk = instance.pk)

@receiver(post_save, sender=SubprofilesGroup)
def after_saving_object_group(sender, instance, created, **kwargs):
    
    user = get_current_user()
    
    if created:
        description = (
            f"Se creó el grupo de usuarios {instance.name}."
        )
        type_change = TypeChanges.objects.get(value="Create")
        
        
    if hasattr(instance, "_old_instance"):
        
        if not instance.is_active:
            
            description = f"Se eliminó el grupo de usuarios {instance.name}."
            type_change = TypeChanges.objects.get(value="Delete")

        else:
            try:
                
                description = create_description(instance, 'SubuserGroup')
                type_change = TypeChanges.objects.get(value="Update")
                
            except sender.DoesNotExist:
                pass
    if description:
    	GroupChanges.objects.create(
    	    main_user=instance.profile.user,
    	    group_changed=instance,
    	    user=user,
    	    type_change=type_change,
    	    description=description,
    	    )
