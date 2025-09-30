from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from Users.models import Profile,Subprofile, TypeChanges, UserChanges, GroupChanges
from .models import Objects,ObjectsGroup,Transaction,GroupObjectsChanges, TypeTransaction
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .functions import create_transaction_description
from .forms import ObjectForm,ObjectsGroupForm,ExportLogForm
from Users.forms import SetImageForm
import openpyxl
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
    
    objects = Objects.objects.filter(user = profile.user if type == 'profile' else profile.profile.user, is_active=True)
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
                    'object_group_form' : ObjectsGroupForm(user=profile.user if type == 'profile' else profile.profile.user),
                    'checked' : 'checked',
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
                    'object_group_form' : form,
                    'checked_group' : 'checked',
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
            return redirect('object_groups')
        

@login_required
def manage_object(request, id):
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
        object = Objects.objects.get(id=id, is_active=True)
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
        if request.POST.get('delete_object', False):
            object.is_active = False
            object.save()
            Transaction.objects.create(
                user = profile.user if type == 'profile' else profile.profile.user,
                type = TypeTransaction.objects.get(name = 'Delete'),
                object = object,
                in_charge = request.user,
                stock_before = object.stock,
                stock_after = 0,
                description = f'Se eliminó el objeto {object.name} que tenía un stock de {object.stock}.',
            )
            messages.success(request, 'El objeto se eliminó con éxito.')
            return redirect('main')
        
        
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
        object = form.save()
        if not 'stock' in form.changed_data:
            type_transaction = TypeTransaction.objects.get(name='Update')
        if int(form.initial['stock']) > object.stock:
            type_transaction = TypeTransaction.objects.get(name='Substract')
        else:
            type_transaction = TypeTransaction.objects.get(name='Add')
        Transaction.objects.create(
            user = profile.user if type == 'profile' else profile.profile.user,
            type = type_transaction,
            object = object,
            in_charge = request.user,
            stock_before = int(form.initial['stock']),
            stock_after = object.stock,
            description = create_transaction_description(object=form.initial,type='Object',updated_data = object.__dict__ ),
            
        )
        messages.success(request, 'Objeto editado correctamente.')
        return redirect('main')

@login_required
def manage_object_groups(request):
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
    
    groups = ObjectsGroup.objects.filter(user = profile.user if type == 'profile' else profile.profile.user, is_active=True)
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
        if request.POST.get('delete_group', False):
            group = ObjectsGroup.objects.get(id = request.POST['id'])
            if Objects.objects.filter(group=group, is_active=True).exists():
                messages.error(request, 'No se puede eliminar el grupo porque hay objetos activos relacionados a él.')
                return redirect('object_groups')
            group.is_active = False
            group.save()
            GroupObjectsChanges.objects.create(
                main_user = profile.user if type == 'profile' else profile.profile.user,
                group_changed = group,
                user = request.user,
                type_change = TypeChanges.objects.get(value='Delete'),
                description = f'Se eliminó el grupo de objetos {group.name}.',
            )
            messages.success(request,'El grupo de objetos se eliminó con éxito.')
            return redirect('object_groups')
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
            form = ObjectsGroupForm(request.POST, user=profile.user if type == 'profile' else profile.profile.user, instance=group)
            changed_fields = form.changed_data
            if not changed_fields:
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
                    'form_post' : form,
                    'group' : group,
                })
            group = form.save()        
            GroupObjectsChanges.objects.create(
                main_user = profile.user if type == 'profile' else profile.profile.user,
                group_changed = group,
                user = request.user,
                type_change = TypeChanges.objects.get(value='Update'),
                description =  create_transaction_description(object=form.initial,type='ObjectGroup',updated_data = group.__dict__ ),
            )
            messages.success(request, 'Grupo de objetos editado correctamente.')
            return redirect('object_groups')

@login_required
def log(request):
    user = request.user
    try:
        profile_admin = profile = Profile.objects.get(user=user)
        type = 'profile'
        permissions = 'admin'
    except ObjectDoesNotExist:
        profile = Subprofile.objects.get(user=user)
        profile_admin = profile.profile
        type = 'subprofile'
        permissions = profile.group.permissions.name
        if permissions == 'Estudiante':
            messages.warning(request, 'No tienes permiso para ver esa página.')
            return redirect('/authenticate_user/deactivate')
    except:
        messages.error(request, 'Hubo un error al tratar de cargar el inventario.')
        return redirect('/authenticate_user/deactivate')

    query_users = UserChanges.objects.filter(main_user=profile_admin.user)
    query_user_groups = GroupChanges.objects.filter(main_user=profile_admin.user)
    query_objects = Transaction.objects.filter(user=profile_admin.user)
    query_object_groups = GroupObjectsChanges.objects.filter(main_user=profile_admin.user)

    if request.method == 'GET':
        return render(request, 'Objects/log.html', {
            'type': type,
            'profile': profile,
            'permissions': permissions,
            'log_users': query_users,
            'log_user_groups': query_user_groups,
            'log_objects': query_objects,
            'log_object_groups': query_object_groups,
            'export_form': ExportLogForm(),
        })
    else:
        form = ExportLogForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Hubo un error al tratar de exportar el inventario.')
            return render(request, 'Objects/log.html', {
                'type': type,
                'profile': profile,
                'permissions': permissions,
                'log_users': query_users,
                'log_user_groups': query_user_groups,
                'log_objects': query_objects,
                'log_object_groups': query_object_groups,
                'export_form': form,
            })
        type = request.POST['type_export']
        
        if type not in ['users','user_groups','objects','object_groups']:
            messages.error(request, 'Hubo un error al tratar de exportar el inventario.')
            return redirect('log')

        match type:
            case 'users':
                log = UserChanges.objects.filter(main_user=request.user,date__range = (request.POST['start_date'], request.POST['end_date']))
                header_object = 'Usuario'  
            case 'user_groups':
                log = GroupChanges.objects.filter(main_user=request.user,date__range = (request.POST['start_date'], request.POST['end_date']))
                header_object = 'Grupo de usuarios'
            case 'objects':
                log = Transaction.objects.filter(user=request.user,date__range = (request.POST['start_date'], request.POST['end_date']))
                header_object = 'Objeto'
            case 'object_groups':
                log =  GroupObjectsChanges.objects.filter(main_user=request.user,date__range = (request.POST['start_date'], request.POST['end_date']))
                header_object = 'Grupo de objetos'
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Log_Inventory_Report"
        
        ws.append([ header_object, 'Tipo de cambio', 'Realizado por', 'Fecha y hora', 'Descripción'])

        for entry in log:
            match type:
                case 'users':
                    object_name = entry.user_changed.username
                    type_change = entry.type_change.value
                case 'user_groups':
                    object_name = entry.group_changed.name
                    type_change = entry.type_change.value
                case 'objects':
                    object_name = entry.object.name
                    type_change = entry.type.name
                case 'object_groups':
                    object_name = entry.group_changed.name
                    type_change = entry.type_change.value
            ws.append([ object_name, type_change, entry.user.username, entry.date.strftime("%Y-%m-%d %H:%M:%S"), entry.description])
        # Prepare response
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="Log_Inventory_Report.xlsx"'

        # Save workbook to response
        wb.save(response)
        return response
        