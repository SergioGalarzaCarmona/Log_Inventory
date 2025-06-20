from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import RegisterUser, LoginUser, RegisterSubuser, RegisterSubprofileGroup, SetImageForm, EditSubprofileForm, EditUserForm, EditSubprofileGroupForm
from .models import Profile, Subprofile, SubprofilesGroup, TypeChanges, UserChanges, GroupChanges
from .functions import create_parameterized_tables, create_description, get_description
from django.core.exceptions import ObjectDoesNotExist

###################################
### ALL VIEWS HAVE DECORATOR @create_parameterized_tables TO CREATE NEEDED ROWS IN PARAMETERIZED TABLES ###
###################################

class Error404View(TemplateView):
    template_name = 'Users/error_404.html'

@create_parameterized_tables
def home(request):
    return render(request, 'Users/home.html')

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
        return render(request, 'Users/authenticate.html', {
            'form': RegisterUser,
            'form_login': LoginUser(request.POST),
            'error': 'Usuario o contraseña incorrectos'
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

@create_parameterized_tables
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

            
def Logout(request):
    logout(request)
    return redirect('home')

@create_parameterized_tables
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
    return render(request, 'Users/main.html',{
        'profile': profile,
        'type' : type,
        'permissions' : permissions
    })

@create_parameterized_tables
@login_required
#View to show the profile of the user, with the form to edit the user
def profile(request,username):
    #verifie that exist one user with this name
    try:
        user = User.objects.get(username=username)
        user_pk = user.pk
    except:
        return render(request, 'Users/error_404.html')  
    #Get user from request to validate if the user is the same that the username in the url
    if request.user != user:
        logout(request)
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
                return render(request, 'Users/profile.html',{
                    'profile': profile,
                    'form' : form,
                    'message': 'Los datos no han sido actualizados.',
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
            return redirect('main')
     
@create_parameterized_tables   
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
            return render(request,'Users/error_403.html')
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
            return redirect('manage_subusers')
        else: 
            form = RegisterSubprofileGroup(request.POST,request.FILES,user_pk = request.user.pk)
            if not form.is_valid():
                    return render(request, 'Users/subusers.html',{
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
            return redirect('manage_subusers')

@create_parameterized_tables
@login_required
def subprofile(request,username):
    #verifie that exist one user with this name
    try:
        subuser = User.objects.get(username=username)
    except:
        return render(request, 'Users/error_404.html')
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
                return redirect('/authenticate_user/deactivate')
        except ObjectDoesNotExist:
            profile = Subprofile.objects.get(user=user)
            type = 'subprofile'
            permissions = profile.group.permissions.name
            if subprofile.profile != profile.profile:
                logout(request)
                return redirect('/authenticate_user/deactivate')
            if permissions == 'Estudiante':
                return render(request, 'Users/error_403.html')
        except:
            return render(request, 'Users/error_404.html')
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
            'permissions' : permissions
        })
    else:
        image = request.FILES.get('image',False)
        delete_image = request.POST.get('delete_image',False)
        if image:
            image_before = subprofile.image.name.split('/')[-1]
            if image_before == 'default.jpg':
                image_before = '""'
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
            return render(request, 'Users/subprofile.html',{
                    'subprofile': subprofile,
                    'profile' : profile,
                    'form' : form,
                    'image_form' : SetImageForm(),
                    'type' : type,
                    'permissions' : permissions
            })
        elif delete_image:
            image_before = subprofile.image.name.split('/')[-1]
            if image_before == 'default.jpg':
                image_before = '""'
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
            return render(request, 'Users/subprofile.html',{
                    'subprofile': subprofile,
                    'profile' : profile,
                    'form' : form,
                    'image_form' : SetImageForm(),
                    'type' : type,
                    'permissions' : permissions
                })
        else:
            form_post = EditUserForm(request.POST,initial=form.initial,instance= user,user_pk = subuser_pk)
            data = form_post.data            
            if user.email == data['email'] and user.username == data['username']:
                return render(request, 'Users/subprofile.html',{
                    'subprofile': subprofile,
                    'profile' : profile,
                    'form' : form,
                    'message': 'Los datos no han sido actualizados.',
                    'image_form' : SetImageForm(),
                    'permissions' : permissions
                })
            if not form_post.is_valid():
                return render(request, 'Users/subprofile.html',{
                    'subprofile': subprofile,
                    'profile' : profile,
                    'form' : form,
                    'form_post' : form_post,
                    'image_form' : SetImageForm(),
                    'type' : type,
                    'permissions' : permissions
            })
            user = User.objects.get(pk=subuser_pk)
            User.objects.filter(pk=subuser_pk).update(username=data['username'],email=data['email']) 
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
            return redirect('manage_subusers')
    
@create_parameterized_tables
@login_required
def subusers_group(request):
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
            return render(request,'Users/error_403.html')
    except:
        return render(request,'Users/error_404.html')
    query_subgroups = SubprofilesGroup.objects.filter(profile=profile_admin)
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
            'groups' : query_subgroups
        })
    else:
        image = request.FILES.get('image',False)
        delete_image = request.POST.get('delete_image',False)
        if image:
            group = SubprofilesGroup.objects.get(pk = request.POST['id'])
            image_before = group.image.name.split('/')[-1]
            if image_before == 'default.jpg':
                image_before = '""'
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
            return render(request,'Users/subprofiles_group.html',{
                'type' : type,
                'profile' : profile,
                'permissions' : permissions,
                'forms' : forms,
                'image_form' : SetImageForm(),
                'groups' : query_subgroups
            })
        elif delete_image:
            group = SubprofilesGroup.objects.get(pk = request.POST['id'])
            image_before = group.image.name.split('/')[-1]
            if image_before == 'default.jpg':
                image_before = '""'
            group.image = 'default.jpg'
            group.save()
            log = TypeChanges.objects.get(value='Update')
            GroupChanges.objects.create(
                    main_user = group.profile.user,
                    group_changed = group,
                    user = request.user,
                    description=f'Change in image, before: "{image_before}", after: ""',
                    type_change = log
            )
            return render(request,'Users/subprofiles_group.html',{
                'type' : type,
                'profile' : profile,
                'permissions' : permissions,
                'forms' : forms,
                'image_form' : SetImageForm(),
                'groups' : query_subgroups
            })
        else:
            group = SubprofilesGroup.objects.get(pk = request.POST['id'])
            form = EditSubprofileGroupForm(instance=group,user_pk=user_pk)
            form_post = EditSubprofileGroupForm(request.POST,instance=group,user_pk=user_pk)
            if request.POST['name'] == group.name and request.POST['permissions'] == str(group.permissions.pk):
                return render(request,'Users/subprofiles_group.html',{
                    'type' : type,
                    'profile' : profile,
                    'permissions' : permissions,
                    'forms' : forms,
                    'form_post' : form_post,
                    'group' : group,
                    'image_form' : SetImageForm(),
                    'groups' : query_subgroups,
                    'message' : 'Los datos no hay sido actualizados'
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
                    'groups' : query_subgroups
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
            return redirect('subusers_group')

@create_parameterized_tables
@login_required
def log_users(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        profile_admin = profile
        type = 'profile'
        permissions = 'admin'
    except ObjectDoesNotExist:
        profile = Subprofile.objects.get(user=user)
        profile_admin = profile.profile
        type = 'subprofile'
        permissions = profile.group.permissions.name
        if permissions == 'Estudiante':
            return render(request,'Users/error_403.html')
    except:
        return render(request,'Users/error_404.html')
    query_users = UserChanges.objects.filter(main_user=profile_admin.user).order_by('-date')
    query_groups = GroupChanges.objects.filter(main_user=profile_admin.user).order_by('-date')
    print(get_description('Change in username, before: Prueba_de_Descripcion, after: Prueba_de_Descripcion2'))
    if request.method == 'GET':
        return render(request,'Users/log_users.html',{
            'type' : type,
            'profile' : profile,
            'permissions' : permissions,
            'log_users' : query_users,
            'log_groups' : query_groups
        })
    else:
        return render(request,'Users/log_users.html',{
            'type' : type,
            'profile' : profile,
            'permissions' : permissions,
            'log_users' : query_users
        })
