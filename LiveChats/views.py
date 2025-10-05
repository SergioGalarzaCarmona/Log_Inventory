from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from Users.models import Profile, Subprofile
from .models import LiveChat
from django.core.exceptions import ObjectDoesNotExist


@login_required
def manage_chats(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
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
    
    chats = LiveChat.objects.filter(admin_user = profile_admin)
    if request.method == 'GET':
        return render('LiveChats/chatsStyles.html',{
            'profile' : profile,
            'type' : type,
            'permissions' : permissions,
        })