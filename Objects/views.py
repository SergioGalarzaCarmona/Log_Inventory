from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Users.models import Profile,Subprofile
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from Users.async_functions import redirect_async,render_async,get_users_log,get_groups_log
from .forms import ObjectForm,ObjectsGroupForm
# Create your views here.

@login_required
#View to show the main page of the app, with the profile of the user
def main(request):
    
    #verifie if the request.user is a profile or a subprofile
    try:
        profile = Profile.objects.get(user=request.user)
        type = 'profile'
        permissions = 'admin'
    except:
        profile = Subprofile.objects.get(user=request.user) 
        type = 'subprofile'
        permissions = profile.group.permissions.name
        
    if request.method == 'GET':
        return render(request, 'Objects/main.html',{
            'profile': profile,
            'type' : type,
            'permissions' : permissions,
            'object_form' : ObjectForm(user=profile.user if type == 'profile' else profile.profile.user),
            'object_group_form' : ObjectsGroupForm(user=profile.user if type == 'profile' else profile.profile.user)
        })
    else:
        object = request.POST.get('stock', None)
        if object:
            form = ObjectForm(request.POST, request.FILES or None, user=profile.user if type == 'profile' else profile.profile.user)
            if not form.is_valid():
                messages.error(request, 'Hubo un error al tratar de crear el objeto.')
                return render(request, 'Objects/main.html',{
                    'profile': profile,
                    'type' : type,
                    'permissions' : permissions,
                    'object_form' : form,
                    'object_group_form' : ObjectsGroupForm(user=profile.user if type == 'profile' else profile.profile.user)
                })
            form.save()
            messages.success(request, 'Objeto creado correctamente.')
            return redirect('main')
        else:
            form = ObjectsGroupForm(request.POST, request.FILES or None,  user=profile.user if type == 'profile' else profile.profile.user)
            if not form.is_valid():
                messages.error(request, 'Hubo un error al tratar de crear el grupo de objetos.')
                return render(request, 'Objects/main.html',{
                    'profile': profile,
                    'type' : type,
                    'permissions' : permissions,
                    'object_form' : ObjectForm(user=profile.user if type == 'profile' else profile.profile.user),
                    'object_group_form' : form
                })
            form.save()
            messages.success(request, 'Grupo de objetos creado correctamente.')
            return redirect('main')
        

@login_required
async def log(request):
    user = request.user
    try:
        profile_admin = profile = await Profile.objects.aget(user=user)
        type = 'profile'
        permissions = 'admin'
    except ObjectDoesNotExist:
        profile = await Subprofile.objects.aget(user=user)
        profile_admin = await profile.profile
        type = 'subprofile'
        permissions = await profile.group.permissions.name
        if permissions == 'Estudiante':
            messages.warning(request,'No tienes permiso para ver esa página.')
            return await redirect_async('/authenticate_user/deactivate')
    except:
        messages.error(request,'Hubo un error al tratar de cargar el inventario.')
        return await redirect_async('/authenticate_user/deactivate')
    query_users = get_users_log(profile_admin)
    query_groups = get_groups_log(profile_admin)
    if request.method == 'GET':
        return await render_async(request,'Objects/log.html',{
            'type' : type,
            'profile' : profile,
            'permissions' : permissions,
            'log_users' : await query_users,
            'log_groups' : await query_groups
        })
    else:
        return await render_async(request,'Objects/log.html',{
            'type' : type,
            'profile' : profile,
            'permissions' : permissions,
            'log_users' : query_users
        })
