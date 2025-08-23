from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Users.models import Profile,Subprofile, TypeChanges
from .models import Objects,ObjectsGroup,Transaction,GroupObjectsChanges, TypeTransaction
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from Users.async_functions import redirect_async, render_async, get_users_log, get_user_groups_log
from .async_functions import get_objects_log, get_object_groups_log
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
    
    objects = Objects.objects.filter(user = profile.user if type == 'profile' else profile.profile.user)
    if request.method == 'GET':
        return render(request, 'Objects/main.html',{
            'profile': profile,
            'type' : type,
            'permissions' : permissions,
            'objects' : objects,
            'object_form' : ObjectForm(user=profile.user if type == 'profile' else profile.profile.user,instance = None),
            'object_group_form' : ObjectsGroupForm(user=profile.user if type == 'profile' else profile.profile.user, instance = None)
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
                    'objects' : objects,
                    'object_form' : form,
                    'object_group_form' : ObjectsGroupForm(user=profile.user if type == 'profile' else profile.profile.user)
                })
            object = form.save(commit = False)
            object.user = profile.user if type == 'profile' else profile.profile.user
            object.save()
            Transaction.objects.create(
                user = profile.user if type == 'profile' else profile.profile.user,
                type = TypeTransaction.objects.get(name='Create'),
                object = object,
                in_charge = request.user,
                stock_before = 0,
                stock_after = object.stock,
                description = f'Se creó el objeto {object.name} con stock inicial de {object.stock}.',
            )
            
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
                    'objects' : objects,
                    'object_form' : ObjectForm(user=profile.user if type == 'profile' else profile.profile.user),
                    'object_group_form' : form
                })
            group = form.save(commit = False)
            group.user = profile.user if type == 'profile' else profile.profile.user
            group.save()            
            GroupObjectsChanges.objects.create(
                main_user = profile.user if type == 'profile' else profile.profile.user,
                group_changed = group,
                user = request.user,
                type_change = TypeChanges.objects.get(value='Create'),
                description = f'Se creó el grupo de objetos {group.name}',
            )
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
    query_user_groups = get_user_groups_log(profile_admin)
    query_objects = get_objects_log(profile_admin)
    query_object_groups = get_object_groups_log(profile_admin)
    
    if request.method == 'GET':
        return await render_async(request,'Objects/log.html',{
            'type' : type,
            'profile' : profile,
            'permissions' : permissions,
            'log_users' : await query_users,
            'log_user_groups' : await query_user_groups,
            'log_objects' : await query_objects,
            'log_object_groups' : await query_object_groups
        })
    else:
        return await render_async(request,'Objects/log.html',{
            'type' : type,
            'profile' : profile,
            'permissions' : permissions,
            'log_users' : query_users
        })
