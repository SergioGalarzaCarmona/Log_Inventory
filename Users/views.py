from django.shortcuts import render,redirect
from .forms import RegisterUser, LoginUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Profile

# Create your views here.
def home(request):
    return render(request, 'Users/home.html')

def start(request):
    if request.method == 'GET':
        return render(request, 'Users/start.html',{
        'SignUpForm': RegisterUser(),
        "LogInForm": LoginUser(),
    })
    else:
        if "SignUp Confirmation" in request.POST:
            confirmation = request.POST.get("SignUp Confirmation", False)
            if confirmation:
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password1'])
                image = request.FILES.get('image','defaul.jpg')
                Profile.objects.create(user=user,image=image)
                return redirect('main')
            form = RegisterUser(request.POST)
            if request.POST['password1'] != request.POST['password2']:
                return render(request, 'Users/start.html', {
                    'SignUpForm': RegisterUser(request.POST,request.FILES),
                    'LogIn-form': LoginUser(request.POST),
                    'messages': 'Las contraseñas no coinciden'
                    })
            if not form.is_valid():
                errors = form.errors
                if 'username' in errors:
                    return render(request, 'Users/start.html', {
                        'SignUpForm': RegisterUser(request.POST,request.FILES),
                        'LogIn-form': LoginUser(request.POST),
                        'messages': errors,
                    }
                    )
            
                return render(request, 'Users/start.html', {
                    'SignUpForm': RegisterUser(request.POST,request.FILES),
                    'LogIn-form': LoginUser(request.POST),
                    'messages': errors,
                })
        
            user = form.save()
            image = request.FILES.get('image','defaul.jpg')
            Profile.objects.create(user=user,image=image)
            return redirect('main')
    
        elif "LogIn Confirmation" in request.POST:
            confirmation = request.POST.get("LogIn Confirmation", False)
            if confirmation:
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                if user is not None:
                    login(request, user)
                    return redirect('main')
                else:
                    return render(request, 'Users/start.html', {
                        'signUp-form': RegisterUser(request.POST,request.FILES),
                        'LogIn-form': LoginUser(request.POST),
                        'messages': 'Usuario o Contraseña Incorrectos',
                    })
            form = LoginUser(request.POST)
            if not form.is_valid():
                errors = form.errors
                return render(request, 'Users/start.html', {
                    'signUp-form': RegisterUser(request.POST,request.FILES),
                    'LogIn-form': LoginUser(request.POST),
                    'messages': errors,
                })
            return render(request, 'Users/start.html', {
                'signUp-form': RegisterUser(request.POST,request.FILES),
                'LogIn-form': LoginUser(request.POST),
                'messages': 'Usuario o Contraseña Incorrectos',
            })

def main(request):
    return render(request, 'Users/main.html')
