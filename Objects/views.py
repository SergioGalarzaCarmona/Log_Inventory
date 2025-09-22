from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from Users.models import Profile,Subprofile, TypeChanges
from .models import Objects,ObjectsGroup,Transaction,GroupObjectsChanges, TypeTransaction
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from Users.async_functions import redirect_async, render_async, get_users_log, get_user_groups_log
from .async_functions import get_objects_log, get_object_groups_log
from .functions import create_transaction_description
from .forms import ObjectForm,ObjectsGroupForm
from Users.forms import SetImageForm
from django.forms.models import model_to_dict
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
def edit_object(request, id):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        type = 'profile'
        permissions = 'admin'
    except ObjectDoesNotExist:
        profile = Subprofile.objects.get(user=user)
        type = 'subprofile'
        permissions = profile.group.permissions.name
    except:
        messages.error(request,'Hubo un error al tratar de cargar el objeto.')
        return redirect('/authenticate_user/deactivate')
    
    try:
        object = Objects.objects.get(id=id)
    except:
        messages.error(request,'No se encontró el objeto que intentas editar.')
        return redirect('main')
    
    if object.user != (profile.user if type == 'profile' else profile.profile.user):
        messages.error(request,'No tienes permiso para editar ese objeto.')
        logout(request)
        return redirect('main')
    image_form = SetImageForm()
    if request.method == 'GET':
        form = ObjectForm(user=profile.user if type == 'profile' else profile.profile.user, instance=object)
        
        if permissions == 'Estudiante':
            for field in form.fields:
                form.fields[field].disabled = True
            for field in image_form.fields:
                image_form.fields[field].disabled = True
        return render(request, 'Objects/object.html',{
            'profile': profile,
            'type' : type,
            'permissions' : permissions,
            'object' : object,
            'object_form' : form,
            'image_form' : image_form,
        })
    else:
        image = request.FILES.get('image',False)
        delete_image = request.POST.get('delete_image',False)
        
        if image:
            image_before = object.image.name
            if image_before == 'default_object.jpg':
                image_before = 'Ninguna'
            object_image = image_before.split('/')[1]
            object.image = image
            object.save()
            Transaction.objects.create(
                user = profile.user if type == 'profile' else profile.profile.user,
                type = TypeTransaction.objects.get(name = 'Update'),
                object = object,
                in_charge = request.user,
                stock_before = object.stock,
                stock_after = object.stock,
                description = f'Cambio en imagen, antes: {object_image} después: {image}.',
            )
            messages.success(request, 'La imagen se cambió con éxito.')
            return redirect('main')
        if delete_image: 
            image_before = object.image.name
            if image_before == 'default_object.jpg':
                messages.error(request, 'No se pudo borrar la imagen ya que el objeto no tenía una imagen relacionada.')
                return redirect(f'/work_space/{id}')
            object_image = image_before.split('/')[1]
            object.image = 'default_object.jpg'
            object.save()
            Transaction.objects.create(
                user = profile.user if type == 'profile' else profile.profile.user,
                type = TypeTransaction.objects.get(name = 'Update'),
                object = object,
                in_charge = request.user,
                stock_before = object.stock,
                stock_after = object.stock,
                description = f'Cambio en imagen, antes: {object_image} después: {image}.',
            )
            messages.success(request, 'La imagen se cambió con éxito.')
            return redirect('main')
        form = ObjectForm(request.POST, request.FILES or None, user=profile.user if type == 'profile' else profile.profile.user, instance=object, initial=object.__dict__)
        if not form.has_changed():
            messages.warning(request, 'No se realizaron cambios porque no había ningun campo editado.')
            return render(request, 'Objects/object.html',{
                'profile': profile,
                'type' : type,
                'permissions' : permissions,
                'object' : object,
                'object_form' : form,
                'image_form': SetImageForm(),
            })
        if not form.is_valid():
            messages.error(request, 'Hubo un error al tratar de editar el objeto.')
            return render(request, 'Objects/object.html',{
                'profile': profile,
                'type' : type,
                'permissions' : permissions,
                'object' : object,
                'object_form' : form,
                'image_form' : SetImageForm(),
            })
            
        stock_before = object.stock
        object = form.save()
        if not 'stock' in form.changed_data:
            type_transaction = TypeTransaction.objects.get(name='Update')
        if stock_before > object.stock:
            type_transaction = TypeTransaction.objects.get(name='Substract')
        else:
            type_transaction = TypeTransaction.objects.get(name='Add')
        Transaction.objects.create(
            user = profile.user if type == 'profile' else profile.profile.user,
            type = type_transaction,
            object = object,
            in_charge = request.user,
            stock_before = stock_before,
            stock_after = object.stock,
            description = create_transaction_description(object=form.initial,updated_data = object.__dict__ ),
            
        )
        messages.success(request, 'Objeto editado correctamente.')
        return redirect('main')

@login_required
def object_groups(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        type = 'profile'
        permissions = 'admin'
    except ObjectDoesNotExist:
        profile = Subprofile.objects.get(user=user)
        type = 'subprofile'
        permissions = profile.group.permissions.name
    except:
        messages.error(request,'Hubo un error al tratar de cargar el inventario.')
        return redirect('/authenticate_user/deactivate')
    
    groups = ObjectsGroup.objects.filter(user = profile.user if type == 'profile' else profile.profile.user)
    forms = []
    for group in groups:
        form = ObjectsGroupForm(user=profile.user if type == 'profile' else profile.profile.user, instance=group)
        if permissions == 'Estudiante':
            for field in form.fields:
                form.fields[field].disabled = True
        forms.append(form)
    if request.method == 'GET':
        return render(request, 'Objects/object_groups.html',{
            'profile': profile,
            'type' : type,
            'permissions' : permissions,
            'object_form' : ObjectForm(user=profile.user if type == 'profile' else profile.profile.user,instance = None),
            'object_group_form' : ObjectsGroupForm(user=profile.user if type == 'profile' else profile.profile.user, instance = None),
            'forms' : forms
        })
    else:
        if image:= request.FILES.get('image', False):
            group = ObjectsGroup.objects.get(id=request.POST['id'])
            group_image_before = group.image.name

            if group_image_before == 'default_object_group.jpg':
                group_image_before = 'Ninguna'
            group.image = image
            group.save()
            GroupObjectsChanges.objects.create(
                main_user = profile.user if type == 'profile' else profile.profile.user,
                group_changed = group,
                user = request.user,
                type_change = TypeChanges.objects.get(value='Update'),
                description = f'Cambio en imagen, antes: {group_image_before} después: {image}.',
            )
            messages.success(request, 'La imagen se cambió con exito')
            return redirect('object_groups')
        if request.POST.get('delete_image', False):
            group = ObjectsGroup.objects.get(id=request.POST['id'])
            group_image_before = group.image.name
            if group_image_before == 'default_object_group.jpg':
                messages.error(request, 'No se pudo borrar la imagen ya que el grupo no tenía una imagen relacionada.')
                return redirect('object_groups')
            group.image = 'default_object_group.jpg'
            group.save()
            GroupObjectsChanges.objects.create(
                main_user = profile.user if type == 'profile' else profile.profile.user,
                group_changed = group,
                user = request.user,
                type_change = TypeChanges.objects.get(value='Update'),
                description = f'Cambio en imagen, antes: {group_image_before} después: Ninguna.',
            )
            messages.success(request, 'La imagen se borró con exito')
            return redirect('object_groups')
        else:
            group = ObjectsGroup.objects.get(id=request.POST['id'])
            initial_data = model_to_dict(group, fields=[field.name for field in group._meta.fields if field.name != 'image'])
            form = ObjectsGroupForm(request.POST, user=profile.user if type == 'profile' else profile.profile.user, instance=group, initial=initial_data)
            if not form.has_changed():
                messages.warning(request, 'No se realizaron cambios porque no había ningun campo editado.')
                return redirect('object_groups')
            if not form.is_valid():
                messages.error(request, 'Hubo un error en los datos ingresados del usuario.')
                return render(request, 'Objects/object_groups.html',{
                    'profile': profile,
                    'type' : type,
                    'permissions' : permissions,
                    'object_form' : ObjectForm(user=profile.user if type == 'profile' else profile.profile.user,instance = None),
                    'object_group_form' : ObjectsGroupForm(user=profile.user if type == 'profile' else profile.profile.user, instance = None),
                    'forms' : forms,
                })
            group = form.save()        
            GroupObjectsChanges.objects.create(
                main_user = profile.user if type == 'profile' else profile.profile.user,
                group_changed = group,
                user = request.user,
                type_change = TypeChanges.objects.get(value='Create'),
                description = f'Se creó el grupo de objetos {group.name}',
            )
            messages.success(request, 'Grupo de objetos editado correctamente.')
            return redirect('object_groups')

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
