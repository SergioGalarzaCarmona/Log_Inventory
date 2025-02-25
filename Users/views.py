from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterUser, LoginUser, RegisterSubuser, RegisterSubprofileGroup, SetImageForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile, SubprofilesGroup
from django.contrib.auth.decorators import login_required
from .forms import EditUserForm
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
    return render(request, 'Users/main.html',{
        'user': request.user
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
            print(request.POST)
            
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
    if request.method == 'GET':
        return render(request, 'Users/subusers.html',{
        'form': RegisterSubuser(user_pk = request.user.pk),
        'group_form': RegisterSubprofileGroup(),
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
                })
            form.create_subprofile()
            return render(request, 'Users/subusers.html',{
            'form': RegisterSubuser(user_pk = request.user.pk),
            'group_form': RegisterSubprofileGroup(),
            })
        else: 
            form = RegisterSubprofileGroup(request,request.POST,request.FILES)
            
            if not form.is_valid():
                if create_subuser:
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
            return redirect('manage_subusers')
