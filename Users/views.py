from django.shortcuts import render,redirect
from .forms import RegisterUser, LoginUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .models import Profile

# Create your views here.
def home(request):
    return render(request, 'Users/home.html')

def logIn(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is None:
         return render(request, 'Users/start.html', {
            'form': RegisterUser,
            'form_login': LoginUser(request.POST),
            'error': 'Usuario o Contraseña Incorrectos',
        })
    else:
        login(request, user)
        return redirect('main')
        
def signUp(request):
    form = RegisterUser(request.POST)
    if request.POST['password1'] != request.POST['password2']:
        return render(request, 'Users/start.html', {
            'form': RegisterUser(request.POST,request.FILES),
            'messages': 'Las contraseñas no coinciden'
            })
    if not form.is_valid():
            return render(request, 'Users/start.html', {
                'form_login': RegisterUser(request.POST,request.FILES),
            })
    user = form.save()
    image = request.FILES.get('image','default.jpg')
    Profile.objects.create(user=user,image=image)
    login(request, user)
    return redirect('main')

def start(request):
    if request.method == 'GET':
        return render(request, 'Users/start.html',{
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

def main(request):
    return render(request, 'Users/main.html',{
        'user': request.user
    })
