from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import RegisterUser, LoginUser, RegisterSubuser, RegisterSubprofileGroup, SetImageForm, EditSubprofileForm, EditUserForm, EditSubprofileGroupForm
from .models import Profile, Subprofile, SubprofilesGroup, TypeChanges, UserChanges, GroupChanges
from .functions import create_parameterized_tables, create_description
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.




class Error404View(TemplateView):
    template_name = 'Users/error_404.html'

@create_parameterized_tables
def home(request):
    return render(request, 'Users/home.html')

#Function used in other view
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
def profile(request,username):
    try:
        user = User.objects.get(username=username)
        user_pk = user.pk
    except:
        return render(request, 'Users/error_404.html')  
    if request.user != user:
        logout(request)
        return redirect('/authenticate_user/deactivate')
    profile = Profile.objects.get(user=request.user)
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
            
            form_post = EditUserForm(request.POST,initial=form.initial,instance= user,user_pk = user_pk)
            data = form_post.data            
            if user.email == data['email'] and user.username == data['username']:
                return render(request, 'Users/profile.html',{
                    'profile': profile,
                    'form' : form,
                    'message': 'Los datos no han sido actualizados.',
                    'image_form' : SetImageForm(),
                    'permissions' : permissions
                })
            if not form_post.is_valid():
                return render(request, 'Users/profile.html',{
                'profile': profile,
                'form' : form,
                'form_post' : form_post,
                'image_form' : SetImageForm(),
                'permissions' : permissions
            })
            user = User.objects.filter(pk=user_pk).update(username=data['username'],email=data['email']) 
            return redirect('main')
     
@create_parameterized_tables   
@login_required
def manage_subusers(request):
    try:
        profile = Profile.objects.get(user=request.user)
        profile_admin = profile        
        permissions = 'admin'
    except:
        profile = Subprofile.objects.get(user=request.user)
        profile_admin = profile.profile
        permissions = profile.group.permissions.name
        if permissions == 'Estudiante':
            return render(request,'Users/error_403.html')
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
            group = form.create_subprofile_group()
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
            UserChanges.objects.create(
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
            group.image = 'default.jpg'
            group.save()
            log = TypeChanges.objects.get(value='Update')
            UserChanges.objects.create(
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
            UserChanges.objects.create(
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


