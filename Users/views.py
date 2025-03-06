from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterUser, LoginUser, RegisterSubuser, RegisterSubprofileGroup, SetImageForm, EditSubprofileForm, EditUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile,Subprofile, SubprofilesGroup
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.exceptions import ValidationError


# Create your views here.


class Error404View(TemplateView):
    template_name = 'Users/error_404.html'


def home(request):
    return render(request, 'Users/home.html')

def logIn(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'], is_active=True)
    if user is not None:
        login(request, user)
        return redirect('main')
    else:
        return render(request, 'Users/authenticate.html', {
            'form': RegisterUser,
            'form_login': LoginUser(request.POST),
            'error': 'Usuario o contraseña incorrectos'
        })
        
def signUp(request):
    class_h2 = "no-margin"
    form = RegisterUser(request.POST)
    if not form.is_valid():
            return render(request, 'Users/authenticate.html', {
                'form': RegisterUser(request.POST,request.FILES),
                'form_login': LoginUser,
                'class' : 'active',
                "class_h2": class_h2,
            })
    user = form.save()
    image = request.FILES.get('image','default.jpg')
    form.create_profile(user,image)
    login(request, user)
    return redirect('main')

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

@login_required
def main(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = Subprofile.objects.get(user=request.user) 
    return render(request, 'Users/main.html',{
        'profile': profile
    })

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
    form = EditUserForm(user_pk = user_pk,instance=user)
    if request.method == 'GET':
        return render(request, 'Users/profile.html',{
            'profile': profile,
            'form' : form,
            'image_form' : SetImageForm()
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
                })
        elif delete_image:
            profile = profile = Profile.objects.get(user=request.user)
            profile.image = 'default.jpg'
            profile.save()
            return render(request, 'Users/profile.html',{
                    'profile': profile,
                    'form' : form,
                    'image_form' : SetImageForm(),
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
                })
            if not form_post.is_valid():
                return render(request, 'Users/profile.html',{
                'profile': profile,
                'form' : form,
                'form_post' : form_post,
                'image_form' : SetImageForm(),
            })
            user = User.objects.filter(pk=user_pk).update(username=data['username'],email=data['email']) 
            return redirect('main')
        
@login_required
def manage_subusers(request):
    profile = Profile.objects.get(user=request.user)
    subusers = Subprofile.objects.filter(profile=profile)
    if request.method == 'GET':
        return render(request, 'Users/subusers.html',{
        'form': RegisterSubuser(user_pk = request.user.pk),
        'group_form': RegisterSubprofileGroup(),
        'subusers': subusers,
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
                })
            subuser = form.save()
            form.create_subprofile(user=subuser,group_id=request.POST['group'],image=request.FILES.get('image','default.jpg'))
            return redirect('manage_subusers')
        else: 
            form = RegisterSubprofileGroup(request.POST,request.FILES,user_pk = request.user.pk)
            
            if not form.is_valid():
                    return render(request, 'Users/subusers.html',{
                    'form': RegisterSubuser(),
                    'form_group': form,
                    'checked_group' : 'checked',
                    'subusers': subusers,
                })
            form.create_subprofile_group()
            return redirect('manage_subusers')

@login_required
def subprofile(request,username):
    try:
        subuser = User.objects.get(username=username)
        user = request.user
        subprofile = Subprofile.objects.get(user=subuser)
        profile = Profile.objects.get(user=user)
        subuser_pk = subuser.pk
    except:
        return render(request, 'Users/error_404.html')  
    if profile != subprofile.profile:
        logout(request)
        return redirect('/authenticate_user/deactivate')
    form = EditSubprofileForm(instance=subuser,user_pk = subuser_pk)
    if request.method == 'GET':
        return render(request, 'Users/subprofile.html',{
            'subprofile': subprofile,
            'form' : form,
            'image_form' : SetImageForm()
        })
    
    