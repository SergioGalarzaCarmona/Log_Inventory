from django.shortcuts import render,redirect
from .forms import RegisterUser
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.
def home(request):
    return render(request, 'Users/home.html')

def sign_up(request):
    if request.method == 'GET':
        return render(request, 'Users/sign_up.html',{
        'form': RegisterUser,
    })
    else:
        confirmation = request.POST.get('Confirmation', False)
        if confirmation:
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password1'])
                image = request.FILES.get('image','defaul.jpg')
                Profile.objects.create(user=user,image=image)
                return redirect('home')
        form = RegisterUser(request.POST)
        if request.POST['password1'] != request.POST['password2']:
            return render(request, 'Users/sign_up.html', {
                'form': RegisterUser(request.POST,request.FILES),
                'messages': 'Las contraseñas no coinciden'
                })
        if not form.is_valid():
            errors = form.errors
            if 'username' in errors:
                return render(request, 'Users/sign_up.html', {
                    'form': RegisterUser(request.POST,request.FILES),
                    'messages': errors,
                }
                )
            
            return render(request, 'Users/sign_up.html', {
                'form': RegisterUser(request.POST,request.FILES),
                'messages': errors,
            })
        
        user = form.save()
        image = request.FILES.get('image','defaul.jpg')
        Profile.objects.create(user=user,image=image)
        return redirect('home')

def main(request):
    return render(request, 'Users/main.html')