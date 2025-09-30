from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Users.models import Profile, Subprofile
from .forms import BorrowingForm
from .models import Borrowings
from Objects.models import Objects


@login_required
def manage_borrowings(request):
    #verifie if the request.user is a profile or a subprofile
    try:
        profile = Profile.objects.get(user=request.user)
        profile_admin = profile    
        permissions = 'admin'
        type = 'profile'
    except:
        profile = Subprofile.objects.get(user=request.user)
        profile_admin = profile.profile
        permissions = profile.group.permissions.name
        type = 'subprofile'
        #if the permissions of the subprofile is 'Estudiante', return a 403 error
        if permissions == 'Estudiante':
            messages.warning(request,'No tienes permiso para ver esa página.')
            return redirect('/authenticate_user/deactivate')
    
    borrowings = Borrowings.objects.filter(in_charge__profile=profile_admin, completed=False)
    subusers = Subprofile.objects.filter(profile=profile_admin)
    objects = Objects.objects.filter(user=profile_admin.user)
    if request.method == 'GET':
        return render(request, 'Borrowings/borrowings.html', {
            'profile': profile,
            'permissions': permissions,
            'type': type,
            'form' : BorrowingForm(user=profile_admin.user),
            'borrowings': borrowings,
            'subusers' : subusers,
            'objects' : objects
        })
    else:
        form = BorrowingForm(request.POST, user=profile_admin.user)
        if not form.is_valid():
            messages.error(request,'Los datos ingresados presentan algun error.')
            return render(request, 'Borrowings/borrowings.html',{
            'profile': profile,
            'permissions': permissions,
            'type': type,
            'form' : form,
            'borrowings': borrowings,
            'subusers' : subusers,
            'objects' : objects
            })
        form.save()
        messages.success(request,'El préstamo se creo con éxito.')
        return redirect('manage_borrowings')