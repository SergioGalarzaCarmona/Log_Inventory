from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from Users.models import Profile, Subprofile, User
from .models import LiveChat
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import Count


@login_required
def manage_chats(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        profile_admin = profile
        type = "profile"
        permissions = "admin"
    except ObjectDoesNotExist:

        profile = Subprofile.objects.get(user=user)
        profile_admin = profile.profile
        type = "subprofile"
        permissions = profile.group.permissions.name
    except:
        logout(request)
        return redirect("authenticate", type="deactivate")
    if permissions != 'Estudiante': 
        subprofiles = Subprofile.objects.filter(profile=profile_admin, is_active = True)
        if permissions == "Profesor":
            subprofiles.exclude(pk=profile.id)
    else:
        subprofiles = Subprofile.objects.filter(profile=profile_admin, is_active = True, group__permissions__name = "Profesor")
    if request.method == "GET":
        return render(
            request,
            "LiveChats/chats.html",
            {
                "profile": profile,
                "type": type,
                "permissions": permissions,
                "subusers": subprofiles,
                "profile_admin" : profile_admin,
            },
        )

@login_required
def live_chat(request, id):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        profile_admin = profile
        type = "profile"
        permissions = "admin"
    except ObjectDoesNotExist:

        profile = Subprofile.objects.get(user=user)
        profile_admin = profile.profile
        type = "subprofile"
        permissions = profile.group.permissions.name
    except:
        logout(request)
        return redirect("authenticate", type="deactivate")

    if permissions != 'Estudiante': 
        subprofiles = Subprofile.objects.filter(profile=profile_admin, is_active = True)
        if permissions == "Profesor":
            subprofiles.exclude(pk=profile.id)
    else:
        subprofiles = Subprofile.objects.filter(profile=profile_admin, is_active = True, group__permissions__name = "Profesor")
    requested_user = User.objects.filter(id=id).first()
    try:
        requested_profile = requested_user.profile
        receiver = requested_user.username
        receiver_username = receiver    
    except:
        requested_subprofile = requested_user.subprofile
        receiver = f'{requested_user.first_name} {requested_user.last_name} '
        receiver_username = requested_user.username
    if requested_user != None:
        chat = LiveChat.objects.filter(users__in=[user, requested_user]) \
            .annotate(num_users=Count("users")) \
            .filter(num_users=2) \
            .first() 
        if chat == None:    
            chat = LiveChat.objects.create(admin_user = profile_admin)
            chat.users.add(user, requested_user)
    messages.success(request, 'Chat abierto con éxito.')
            
    
    
    if request.method == "GET":
        return render(request,
            "LiveChats/chats.html",
            {
                "profile": profile,
                "type": type,
                "permissions": permissions,
                "subusers": subprofiles,
                'chat' : chat,
                "profile_admin" : profile_admin,
                'receiver' : receiver,
                'receiver_username' : receiver_username
            })
    
        