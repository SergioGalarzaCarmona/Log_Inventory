from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterUser, LoginUser, RegisterSubuser, RegisterSubprofileGroup, SetImageForm, EditSubprofileForm, EditUserForm, EditSubprofileGroupForm, SetPassword
from .models import Profile, Subprofile, SubprofilesGroup, TypeChanges, UserChanges, GroupChanges, UserSession
from .functions import create_description
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
###################################
### ALL VIEWS HAVE DECORATOR TO CREATE NEEDED ROWS IN PARAMETERIZED TABLES ###
###################################

class UserPasswordChangeView(PasswordChangeView):
    success_url = '/work_space/'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "La constraseña se cambió con éxito.")
        UserSession.objects.update_or_create(
            user=self.request.user,
            defaults={'session_key' : self.request.session.session_key}
        )
        return response

def home(request):
    return render(request, 'Users/home.html')

def Logout(request):
    logout(request)
    return redirect('home')


#Function to log in user on app
def logIn(request):
    #authenticate user
    user = authenticate(username=request.POST['username'], password=request.POST['password'], is_active=True)
    #If find user and two values are corrects, log in.
    if user is not None:
        login(request, user)
        return redirect('main')
    #if not find user, return a error message 
    else:
        messages.error(request,'Usuario o contraseña incorrectos')
        return render(request, 'Users/authenticate.html', {
            'form': RegisterUser(),
            'form_login': LoginUser(request.POST)
        })

#Function to register users on app
def signUp(request):
    #str with one css class
    class_h2 = "no-margin"
    #create form to register user
    form = RegisterUser(request.POST)
    #if only one value of form is invalid, return the error message, and css class for fix error of margin
    if not form.is_valid():
            return render(request, 'Users/authenticate.html', {
                'form': RegisterUser(request.POST,request.FILES),
                'form_login': LoginUser,
                'class' : 'active',
                "class_h2": class_h2,
            })
    #if all form is valid, save it to create an user.
    user = form.save()
    #If the user uploads an image, the image will have that value, otherwise, it will have a default value.
    image = request.FILES.get('image','default.jpg')
    #with user and image create a profile
    form.create_profile(user,image)
    #login the user
    login(request, user)
    return redirect('main')

#View to manage log in ang register of users
def authenticate_user(request,type):
    if request.method == 'GET':
        return render(request, 'Users/authenticate.html',{
        'form': RegisterUser,
        'form_login': LoginUser,
        'class' : type,
        })
    else:
        sign_up = request.POST.get('signup', False)
        if sign_up:
            return signUp(request)
        return logIn(request)

@login_required
#View to show the profile of the user, with the form to edit the user
def profile(request,username):
    #verifie that exist one user with this name
    try:
        user = User.objects.get(username=username)
        user_pk = user.pk
    except:
        messages.error(request,'El usuario no existe.')
        return redirect('/authenticate_user/deactivate')
    #Get user from request to validate if the user is the same that the username in the url
    if request.user != user:
        logout(request)
        messages.warning(request,'No tienes permiso para ver ese usuario.')
        return redirect('/authenticate_user/deactivate')
    #Get profile from the user
    profile = Profile.objects.get(user=request.user)
    #Always the user permissions is admin, because the profile is main account
    permissions = 'admin'
    form = EditUserForm(user_pk = user_pk,instance=user)
    if request.method == 'GET':
        return render(request, 'Users/profile.html',{
            'profile': profile,
            'form' : form,
            'image_form' : SetImageForm(),
            'type' : 'profile',
            'permissions' : permissions
        })
    else:
        #Verifie what type of request is, if is a image(to update image) or delete image, or update user data
        image = request.FILES.get('image',False)
        delete_image = request.POST.get('delete_image',False)
        if image:
            profile = Profile.objects.get(user=request.user)
            profile.image = image
            profile.save()
            messages.success(request,'La imagen se cambió con exito.')
            return render(request, 'Users/profile.html',{
                    'profile': profile,
                    'form' : form,
                    'image_form' : SetImageForm(),
                    'type' : 'profile',
                    'permissions' : permissions
                })
        elif delete_image:
            profile = Profile.objects.get(user=request.user)
            profile.image = 'default.jpg'
            profile.save()
            messages.success(request,'La imagen se borró con exito.')
            return render(request, 'Users/profile.html',{
                    'profile': profile,
                    'form' : form,
                    'image_form' : SetImageForm(),
                    'type' : 'profile',
                    'permissions' : permissions
                })
        else:
            #Create a new form with the data of the request.POST, and the initial data of the form
            form_post = EditUserForm(request.POST,initial=form.initial,instance= user,user_pk = user_pk)
            data = form_post.data         
            #if the user email and username are the same that the data of the form, return a message that the data has not been updated   
            if user.email == data['email'] and user.username == data['username']:
                messages.error(request,'Los datos no han sido actualizados.')
                return render(request, 'Users/profile.html',{
                    'profile': profile,
                    'form' : form,
                    'image_form' : SetImageForm(),
                    'permissions' : permissions
                })
            #if the form is not valid, return the form with the errors
            if not form_post.is_valid():
                return render(request, 'Users/profile.html',{
                'profile': profile,
                'form' : form,
                'form_post' : form_post,
                'image_form' : SetImageForm(),
                'permissions' : permissions
            })
            #if the form is valid, update the user with the data of the form
            user = User.objects.filter(pk=user_pk).update(username=data['username'],email=data['email']) 
            messages.success(request,'Los datos se actualizaron con éxito.')
            return redirect('main')
        
@login_required
#view to manage subusers 
def manage_subusers(request):
    #verifie if the request.user is a profile or a subprofile
    try:
        profile = Profile.objects.get(user=request.user)
        profile_admin = profile        
        permissions = 'admin'
    except:
        profile = Subprofile.objects.get(user=request.user)
        profile_admin = profile.profile
        permissions = profile.group.permissions.name
        #if the permissions of the subprofile is 'Estudiante', return a 403 error
        if permissions == 'Estudiante':
            messages.warning(request,'No tienes permiso para ver esa página.')
            return redirect('/authenticate_user/deactivate')
    #Get all subusers of the profile(main account)
    subusers = Subprofile.objects.filter(profile=profile_admin)
    if request.method == 'GET':
        return render(request, 'Users/subusers.html',{
        'form': RegisterSubuser(user_pk = request.user.pk),
        'group_form': RegisterSubprofileGroup(),
        'subusers': subusers,
        'profile' : profile,
        'type' : 'profile',
        'permissions' : permissions
    })
    else:
        #Get the username from the request.POST, if exist, is to create a subuser, if not, is to create a subprofile group
        create_subuser = request.POST.get('username', False)
        if create_subuser:
            form = RegisterSubuser(request.POST,request.FILES,user_pk = request.user.pk)
            if not form.is_valid():
                return render(request, 'Users/subusers.html',{
                    'form': form,
                    'group_form': RegisterSubprofileGroup(),
                    'checked' : 'checked',
                    'subusers': subusers,
                    'profile' : profile,
                    'type' : 'profile',
                    'permissions' : permissions
                })
            subuser = form.save()
            form.create_subprofile(user=subuser,group_id=request.POST['group'],image=request.FILES.get('image','default.jpg'))
            log = TypeChanges.objects.get(value='Create')
            UserChanges.objects.create(
                main_user=profile_admin.user,
                user_changed = subuser,
                user = request.user,
                description=f'Creating subuser {subuser.username} with group {subuser.subprofile.group.name}',
                type_change=log)
            messages.success(request,'El usuario se creó con éxito.')
            return redirect('manage_subusers')
        else: 
            form = RegisterSubprofileGroup(request.POST,request.FILES,user_pk = request.user.pk)
            if not form.is_valid():
                    return render(request, 'Users/subprofiles_group.html',{
                    'form': RegisterSubuser(user_pk = request.user.pk),
                    'group_form': form,
                    'checked_group' : 'checked',
                    'subusers': subusers,
                    'profile' : profile,
                    'type' : 'profile',
                    'permissions' : permissions
                })
            group = form.create_subprofile_group(image=request.FILES.get('image','default_group.jpg'))
            log = TypeChanges.objects.get(value='Create')
            GroupChanges.objects.create(
                main_user=profile_admin.user,
                group_changed = group,
                user = request.user,
                description=f'Creating group {group.name} with permissions {group.permissions.name}',
                type_change=log)
            messages.success(request,'El grupo se creó con éxito.')
            return redirect('subusers_group')

@login_required
def subprofile(request,username):
    #verifie that exist one user with this name
    try:
        subuser = User.objects.get(username=username)
    except:
        messages.error(request,'El usuario no existe.')
        return redirect('/authenticate/deactivate')
    #Get user 
    user = request.user
    if subuser != user:
        #get subprofile from the subuser
        subprofile = Subprofile.objects.get(user=subuser)
        subuser_pk = subuser.pk
        #try get profile from the user, if raise a exception in the next try 
        try:
            profile = user.profile
            type = 'profile'
            permissions = 'admin'
            if subprofile.profile != profile:
                logout(request)
                messages.warning(request,'No tienes permiso para ver información acerca de ese usuario.')
                return redirect('/authenticate_user/deactivate')
        except ObjectDoesNotExist:
            profile = Subprofile.objects.get(user=user)
            type = 'subprofile'
            permissions = profile.group.permissions.name
            if subprofile.profile != profile.profile:
                logout(request)
                messages.warning(request,'No tienes permiso para ver información acerca de ese usuario.')
                return redirect('/authenticate_user/deactivate')
            if permissions == 'Estudiante':
                messages.warning(request,'No tienes permiso para ver información de otros usuarios.')
                return redirect('/authenticate_user/deactivate')
        except:
            messages.error(request,'El usuario no existe.')
            return redirect('main')
    else:
        subprofile = Subprofile.objects.get(user=subuser)
        subuser_pk = subuser.pk
        permissions = subprofile.group.permissions.name
        type = 'subprofile'
        profile = user.subprofile
    form = EditSubprofileForm(instance=subuser,user_pk = subuser_pk,permissions = permissions)
    if request.method == 'GET':
        return render(request, 'Users/subprofile.html',{
            'subprofile': subprofile,
            'profile' : profile,
            'form' : form,
            'image_form' : SetImageForm(),
            'type' : type,
            'permissions' : permissions,
            'password_form' : SetPassword(user=subuser),
        })
    else:
        image = request.FILES.get('image',False)
        delete_image = request.POST.get('delete_image',False)
        change_password = request.POST.get("new_password2",'')
        if change_password == '':
            change_password = False
        if image:
            image_before = subprofile.image.name
            if image_before == 'default.jpg':
                image_before = ''
            subprofile.image = image
            subprofile.save()
            log = TypeChanges.objects.get(value='Update')
            UserChanges.objects.create(
                main_user = subprofile.profile.user,
                user_changed = subprofile.user,
                user = request.user,
                description=f'Change in image, before: {image_before}, after: {image}',
                type_change = log
            )
            messages.success(request,'La iamgen se cambió con éxito.')
            return render(request, 'Users/subprofile.html',{
                    'subprofile': subprofile,
                    'profile' : profile,
                    'form' : form,
                    'image_form' : SetImageForm(),
                    'type' : type,
                    'permissions' : permissions,
                    'password_form' : SetPassword(user=subuser),
            })
        elif delete_image:
            image_before = subprofile.image.name
            if image_before == 'default.jpg':
                image_before = ''
            subprofile.image = 'default.jpg'
            subprofile.save()
            log = TypeChanges.objects.get(value='Update')
            UserChanges.objects.create(
                main_user = subprofile.profile.user,
                user_changed = subprofile.user,
                user = request.user,
                description=f'Change in image, before: "{image_before}", after: ""',
                type_change = log
            )
            messages.success(request,'La imagen se borró con éxito.')
            return render(request, 'Users/subprofile.html',{
                    'subprofile': subprofile,
                    'profile' : profile,
                    'form' : form,
                    'image_form' : SetImageForm(),
                    'type' : type,
                    'permissions' : permissions,
                    'password_form' : SetPassword(user=subuser),
                })
        else:
            
            form_post = EditSubprofileForm(request.POST,initial=form.initial,instance=subuser,user_pk = subuser_pk,permissions=permissions)
            data = form_post.data
            
            if not form_post.has_changed() and change_password == False:
                messages.error(request,'Los datos no han sido actualizados.')
                return render(request, 'Users/subprofile.html',{
                    'subprofile': subprofile,
                    'profile' : profile,
                    'form' : form,
                    'image_form' : SetImageForm(),
                    'permissions' : permissions,
                    'password_form' : SetPassword(user=subuser),
                })
            if change_password:
                password_form = SetPassword(user=subuser,data=request.POST)
                if not password_form.is_valid():
                    messages.warning(request,'Hubo un error al cambiar la contraseña, todos los demás posibles datos ingresados no se guardarán.')
                    return render(request, 'Users/subprofile.html',{
                        'subprofile': subprofile,
                        'profile' : profile,
                        'form' : form,
                        'form_post' : form_post,
                        'image_form' : SetImageForm(),
                        'type' : type,
                        'permissions' : permissions,
                        'password_form' : password_form,
                    })
                password_form.save()
                log = TypeChanges.objects.get(value='Update')
                UserChanges.objects.create(
                    main_user = subprofile.profile.user,
                    user_changed = subuser,
                    user = request.user,
                    description=f'Change in password',
                    type_change = log
                )
                messages.success(request,'La contraseña se cambió con exito.')
            if not form_post.is_valid():
                return render(request, 'Users/subprofile.html',{
                    'subprofile': subprofile,
                    'profile' : profile,
                    'form' : form,
                    'form_post' : form_post,
                    'image_form' : SetImageForm(),
                    'type' : type,
                    'permissions' : permissions,
                    'password_form' : SetPassword(user=subuser),
            })
            
            user = User.objects.get(pk=subuser_pk)
            User.objects.filter(pk=subuser_pk).update(username=data['username'],email=data['email']) 
            try:
                Subprofile.objects.filter(user=user).update(group=data['group'])
            except:
                pass
            log = TypeChanges.objects.get(value='Update')
            UserChanges.objects.create(
                main_user = user.subprofile.profile.user,
                user_changed = user,
                user = request.user,
                description=create_description(
                    object=user,
                    type = 'Subuser',
                    username = data['username'],
                    email = data['email'],
                    group = user.subprofile.group.name
                    ),
                type_change = log
            )
            messages.success(request,'Los datos se actualizaron con éxito.')
            if permissions == 'admin' or permissions == 'Profesor':
                return redirect('manage_subusers')
            else:
                return redirect('main')
    
@login_required
def manage_subusers_group(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        profile_admin = profile
        user_pk = user.pk
        type = 'profile'
        permissions = 'admin'
    except ObjectDoesNotExist:
        profile = Subprofile.objects.get(user=user)
        profile_admin = profile.profile
        user_pk = profile.profile.user.pk
        type = 'subprofile'
        permissions = profile.group.permissions.name
        if permissions == 'Estudiante':
            messages.warning(request,'No tienes permiso para ver esa página.')
            return redirect('/authenticate_user/deactivate/')
    except:
        messages.error(request,'Hubo un error al tratar de cargar los grupos.')
        return redirect('/authenticate_user/deactivate/')
    query_subgroups = SubprofilesGroup.objects.filter(profile=profile_admin, is_active=True)
    forms = []
    for group in query_subgroups:
        form = EditSubprofileGroupForm(instance=group,user_pk=user_pk)
        forms.append(form)
    if request.method == 'GET':
        return render(request,'Users/subprofiles_group.html',{
            'type' : type,
            'profile' : profile,
            'permissions' : permissions,
            'forms' : forms,
            'image_form' : SetImageForm(),
            'groups' : query_subgroups,
            'subuser_form': RegisterSubuser(user_pk = request.user.pk),
            'group_form': RegisterSubprofileGroup(),
        })
    else:
        image = request.FILES.get('image',False)
        delete_image = request.POST.get('delete_image',False)
        delete_group = request.POST.get('delete_group',False)
        if image:
            group = SubprofilesGroup.objects.get(pk = request.POST['id'])
            image_before = group.image.name
            if image_before == 'default_group.jpg':
                image_before = ''
            group.image = image
            group.save()
            log = TypeChanges.objects.get(value='Update')
            GroupChanges.objects.create(
                main_user = group.profile.user,
                group_changed = group,
                user = request.user,
                description=f'Change in image, before: {image_before}, after: {image}',
                type_change = log
            )
            messages.success(request,'La imagen se cambió con éxito.')
            return redirect('subusers_group')
        elif delete_image:
            group = SubprofilesGroup.objects.get(pk = request.POST['id'])
            image_before = group.image.name
            if image_before == 'default_group.jpg':
                image_before = ''
            group.image = 'default_group.jpg'
            group.save()
            log = TypeChanges.objects.get(value='Update')
            GroupChanges.objects.create(
                    main_user = group.profile.user,
                    group_changed = group,
                    user = request.user,
                    description=f'Change in image, before: "{image_before}", after: ""',
                    type_change = log
            )
            messages.success(request,'La imagen se borró con éxito.')
            return redirect('subusers_group')
        elif delete_group:
            group = SubprofilesGroup.objects.get(pk = request.POST['id'])
            subprofiles = Subprofile.objects.filter(group=group)
            if subprofiles.count() > 0:
                messages.error(request,'No se puede eliminar el grupo porque tiene subusuarios asociados.')
                return render(request,'Users/subprofiles_group.html',{
                    'type' : type,
                    'profile' : profile,
                    'permissions' : permissions,
                    'forms' : forms,
                    'image_form' : SetImageForm(),
                    'groups' : query_subgroups,
                    'subuser_form': RegisterSubuser(user_pk = request.user.pk),
                    'group_form': RegisterSubprofileGroup(),
                })
            log = TypeChanges.objects.get(value='Delete')
            GroupChanges.objects.create(
                main_user=profile_admin.user,
                group_changed = group,
                user = request.user,
                description=f'Delete group {group.name} with permissions {group.permissions.name}',
                type_change=log)
            group.is_active = False
            group.save()
            messages.success(request,'El grupo se borró con éxito.')
            return redirect('subusers_group')
        else:
            group = SubprofilesGroup.objects.get(pk = request.POST['id'])
            form = EditSubprofileGroupForm(instance=group,user_pk=user_pk)
            form_post = EditSubprofileGroupForm(request.POST,instance=group,user_pk=user_pk)
            if request.POST['name'] == group.name and request.POST['permissions'] == str(group.permissions.pk) and request.POST['description'] == group.description:
                messages.error(request,'Los datos no han sido actualizados.')
                return render(request,'Users/subprofiles_group.html',{
                    'type' : type,
                    'profile' : profile,
                    'permissions' : permissions,
                    'forms' : forms,
                    'form_post' : form_post,
                    'group' : group,
                    'image_form' : SetImageForm(instance=group),
                    'groups' : query_subgroups,
                    'subuser_form': RegisterSubuser(user_pk = request.user.pk),
                    'group_form': RegisterSubprofileGroup(),
                })
            if not form_post.is_valid():
                return render(request,'Users/subprofiles_group.html',{
                    'type' : type,
                    'profile' : profile,
                    'permissions' : permissions,
                    'forms' : forms,
                    'form_post' : form_post,
                    'group' : group,
                    'image_form' : SetImageForm(),
                    'groups' : query_subgroups,
                    'subuser_form': RegisterSubuser(user_pk = request.user.pk),
                    'group_form': RegisterSubprofileGroup(),
                })
            form_post.save()
            log = TypeChanges.objects.get(value='Update')
            GroupChanges.objects.create(
                main_user=profile_admin.user,
                group_changed = group,
                user = request.user,
                description=create_description(
                    object=group,
                    type = 'SubuserGroup',
                    name = request.POST['name'],
                    permissions = request.POST['permissions']
                    ),
                type_change=log)
            messages.success(request,'Los datos se actualizaron con éxito.')
            return redirect('subusers_group')

