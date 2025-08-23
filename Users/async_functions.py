from asgiref.sync import sync_to_async
from .models import UserChanges,GroupChanges
from django.shortcuts import render,redirect


@sync_to_async
def get_users_log(profile_admin):
    return UserChanges.objects.filter(main_user=profile_admin.user).order_by('-date')

@sync_to_async
def get_user_groups_log(profile_admin):
    return GroupChanges.objects.filter(main_user=profile_admin.user).order_by('-date')
    

@sync_to_async
def render_async(request,template,context=None):
    return render(request,template,context)

@sync_to_async
def redirect_async(url):
    return redirect(url)
