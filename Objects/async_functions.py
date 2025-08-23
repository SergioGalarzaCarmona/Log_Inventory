from asgiref.sync import sync_to_async

@sync_to_async
def get_objects_log(profile_admin:object):
    from .models import Transaction
    return Transaction.objects.filter(user = profile_admin.user)

@sync_to_async
def get_object_groups_log(profile_admin:object):
    from .models import GroupObjectsChanges
    return GroupObjectsChanges.objects.filter(main_user = profile_admin.user)