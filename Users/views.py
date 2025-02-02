from django.shortcuts import render,redirect
from .forms import RegisterUser, LoginUser, RegisterSubuser, RegisterSubprofileGroup
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Subprofile, SubprofilesGroup
from django.contrib.auth.decorators import login_required
from .forms import EditUserForm
from django import forms

# Create your views here.
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
    form.create_profile(user)
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
    return render(request, 'Users/main.html',{
        'user': request.user
    })

@login_required
def profile(request,username):
    user = User.objects.get(username=username)
    if request.user != user:
        logout(request)
        return redirect('/authenticate_user/deactivate')
    profile = Profile.objects.get(user=request.user)
    form = EditUserForm(instance=user)
    if request.method == 'GET':
        return render(request, 'Users/profile.html',{
            'profile': profile,
            'form' : form
        })
    else:
        return render(request, 'Users/profile.html',{
            'profile': profile
        })
        
@login_required
def manage_subusers(request):
    if request.method == 'GET':
        return render(request, 'Users/subusers.html',{
        'form': RegisterSubuser(request),
    })
    else:
        create = request.POST.get('username', False)
        if create:
            form = RegisterSubuser(request,request.POST,request.FILES)
            subprofile = form.create_subprofile(commit=False)
        else: 
            form = RegisterSubprofileGroup(request,request.POST,request.FILES)
            
            if not form.is_valid():
                if create:
                    return render(request, 'Users/subusers.html',{
                    'form': form,
                    'created_subgroup' : 'checked',
                })
                else:
                    return render(request, 'Users/subusers.html',{
                    'form': RegisterSubuser(request),
                    'form_group': form,
                    'created_subgroup' : 'checked',
                })
            subprofile.save()
            SubprofilesGroup.objects.create(profile_id=Profile.objects.get(user=request.user),subprofile_id=subprofile,name='',image='',permissions_id=1)
            return redirect('manage_subusers')
        