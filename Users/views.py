from django.shortcuts import render,redirect
from .forms import RegisterUser, LoginUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .models import Profile
from django.contrib.auth.decorators import login_required

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
    class_container = 'active'
    class_h2 = "no-margin"
    form = RegisterUser(request.POST)
    registered_email = User.objects.filter(email=request.POST['email'])
    if len(registered_email) != 0:
        return render(request, 'Users/authenticate.html', {
            'form': RegisterUser(request.POST,request.FILES),
            'form_login': LoginUser,
            'messages': 'El correo ya esta registrado',
            'class' : class_container
            })
    if not form.is_valid():
            return render(request, 'Users/authenticate.html', {
                'form': RegisterUser(request.POST,request.FILES),
                'form_login': LoginUser,
                'class' : class_container,
                "class_h2": class_h2,
            })
    user = form.save()
    image = request.FILES.get('image','default.jpg')
    Profile.objects.create(user=user,image=image)
    login(request, user)
    return redirect('main')

def authenticate_user(request):
    if request.method == 'GET':
        return render(request, 'Users/authenticate.html',{
        'form': RegisterUser,
        'form_login': LoginUser,
        })
    else:
        sign_up = request.POST.get('signup', False)
        confirmation = request.POST.get('confirmation', False)
        if sign_up or confirmation:
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
