from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import (
    RegisterUser,
    RegisterSubuser,
    RegisterSubprofileGroup,
    SetImageForm,
    EditSubprofileForm,
    EditUserForm,
    EditSubprofileGroupForm,
    SetPassword,
)
from .models import (
    Profile,
    Subprofile,
    SubprofilesGroup,
    TypeChanges,
    UserChanges,
    GroupChanges,
    UserSession,
)
from .functions import create_description
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from Objects.models import Objects, ObjectsGroup
from django.db.models import Q


# Email imports
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .functions import account_activation_token

###################################
### ALL VIEWS HAVE DECORATOR TO CREATE NEEDED ROWS IN PARAMETERIZED TABLES ###
###################################


class UserPasswordChangeView(PasswordChangeView):
    success_url = "/work_space/"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "La constraseña se cambió con éxito.")
        UserSession.objects.update_or_create(
            user=self.request.user,
            defaults={"session_key": self.request.session.session_key},
        )
        return response


def home(request):
    return render(request, "Users/home.html")


def Logout(request):
    logout(request)
    return redirect("home")


# Function to log in user on app
def logIn(request):
    # authenticate user
    try:
        user = User.objects.get(email=request.POST["email"])
    except ObjectDoesNotExist:
        messages.error(request, "Usuario o contraseña incorrectos")
        return render(request, "Users/authenticate.html", {"form": RegisterUser()})
    user = authenticate(username=user.username, password=request.POST["password"])
    # If find user and two values are corrects, log in.
    if user is not None and user.is_active == True:
        login(request, user)
        return redirect("main")
    # if not find user, return a error message
    else:
        messages.error(request, "Usuario o contraseña incorrectos")
        return render(request, "Users/authenticate.html", {"form": RegisterUser()})


# Function to register users on app
def signUp(request):
    # str with one css class
    class_h2 = "no-margin"
    # create form to register user
    form = RegisterUser(request.POST)
    # if only one value of form is invalid, return the error message, and css class for fix error of margin
    if not form.is_valid():
        return render(
            request,
            "Users/authenticate.html",
            {
                "form": form,
                "class": "active",
                "class_h2": class_h2,
            },
        )
    # if all form is valid, save it to create an user.
    user = form.save()
    # If the user uploads an image, the image will have that value, otherwise, it will have a default value.
    image = request.FILES.get("image", "default.jpg")
    # with user and image create a profile
    form.create_profile(user, image)
    user.is_active = False
    user.save()

    current_site = get_current_site(request)
    subject = "Activa tu cuenta"
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    activation_link = f"http://{current_site.domain}{reverse('activate', kwargs={'uidb64': uid, 'token': token})}"
    message = render_to_string(
        "activation_email.html",
        {
            "user": user,
            "activation_link": activation_link,
        },
    )
    send_mail(
        subject,
        message,
        None,
        [user.email],
        fail_silently=False,
    )
    messages.warning(
        request,
        "Se te mandó un correo de verificación, para iniciar sesión primero verifica tu cuenta",
    )
    return redirect("authenticate", type="deactivate")

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Tú cuenta ha sido validada exitosamente!")
        return redirect("authenticate", type="deactivate")
    else:
        messages.error(request, "Link de activación expirado o inválida.")
        return redirect("authenticate", type="activate")

# View to manage log in ang register of users
def authenticate_user(request, type):
    if request.method == "GET":
        return render(
            request,
            "Users/authenticate.html",
            {
                "form": RegisterUser,
                "class": type,
            },
        )
    else:
        sign_up = request.POST.get("signup", False)
        if sign_up:
            return signUp(request)
        return logIn(request)


@login_required
# View to show the profile of the user, with the form to edit the user
def profile(request, id):
    # verifie that exist one user with this id
    try:
        user = User.objects.get(id=id)
        user_pk = user.pk
    except:
        messages.error(request, "El usuario no existe.")
        logout(request)
        return redirect("authenticate", type="deactivate")
    # Get user from request to validate if the user is the same that the username in the url
    if request.user != user:
        logout(request)
        messages.warning(request, "No tienes permiso para ver ese usuario.")
        return redirect("authenticate", type="deactivate")
    # Get profile from the user
    profile = Profile.objects.get(user=request.user)
    # Always the user permissions is admin, because the profile is main account
    permissions = "admin"
    form = EditUserForm(user_pk=user_pk, instance=user)
    if request.method == "GET":
        return render(
            request,
            "Users/profile.html",
            {
                "profile": profile,
                "form": form,
                "image_form": SetImageForm(),
                "type": "profile",
                "permissions": permissions,
            },
        )
    else:
        # Verifie what type of request is, if is a image(to update image) or delete image, or update user data
        image = request.FILES.get("image", False)
        delete_image = request.POST.get("delete_image", False)
        if image:
            profile = Profile.objects.get(user=request.user)
            profile.image = image
            profile.save()
            messages.success(request, "La imagen se cambió con exito.")
            return redirect(f"/profile/{id}")
        elif delete_image:
            profile = Profile.objects.get(user=request.user)
            if profile.image.name == "default.jpg":
                messages.error(
                    request,
                    "No se pudo cambiar la imagen porque no tienes ninguna imagen relacionada a tu perfil.",
                )
            profile.image = "default.jpg"
            profile.save()
            messages.success(request, "La imagen se borró con exito.")
            return redirect(f"/profile/{id}")
        else:
            # Create a new form with the data of the request.POST, and the initial data of the form
            form_post = EditUserForm(
                request.POST, initial=form.initial, instance=user, user_pk=user_pk
            )
            data = form_post.data
            # if the user email and username are the same that the data of the form, return a message that the data has not been updated
            if user.email == data["email"] and user.username == data["username"]:
                messages.warning(request, "Los datos no han sido actualizados.")
                return render(
                    request,
                    "Users/profile.html",
                    {
                        "profile": profile,
                        "form": form,
                        "image_form": SetImageForm(),
                        "permissions": permissions,
                        "type": "profile"
                    },
                )
            # if the form is not valid, return the form with the errors
            if not form_post.is_valid():
                return render(
                    request,
                    "Users/profile.html",
                    {
                        "profile": profile,
                        "form": form,
                        "form_post": form_post,
                        "image_form": SetImageForm(),
                        "permissions": permissions,
                        "type": "profile"
                    },
                )
            # if the form is valid, update the user with the data of the form
            user = User.objects.filter(pk=user_pk).update(
                username=data["username"], email=data["email"]
            )
            messages.success(request, "Los datos se actualizaron con éxito.")
            return redirect("main")


@login_required
# view to manage subusers
def manage_subusers(request):
    # verifie if the request.user is a profile or a subprofile
    try:
        profile = Profile.objects.get(user=request.user)
        profile_admin = profile
        type = 'profile'
        permissions = "admin"
    except:
        profile = Subprofile.objects.get(user=request.user)
        profile_admin = profile.profile
        type = 'subprofile'
        permissions = profile.group.permissions.name
        # if the permissions of the subprofile is 'Estudiante', return a 403 error
        if permissions == "Estudiante":
            messages.warning(request, "No tienes permiso para ver esa página.")
            return redirect("authenticate", type="deactivate")
    # Get all subusers of the profile(main account)
    if type == "profile":
        subusers = Subprofile.objects.filter(profile=profile_admin, is_active=True)
    else:
        subusers = Subprofile.objects.filter(profile=profile_admin, is_active=True).exclude(group__permissions__name=permissions)
    if request.method == "GET":
        return render(
            request,
            "Users/subusers.html",
            {
                "form": RegisterSubuser(user_pk=request.user.pk),
                "group_form": RegisterSubprofileGroup(),
                "subusers": subusers,
                "profile": profile,
                "type": type,
                "permissions": permissions,
            },
        )
    else:
        # Get the username from the request.POST, if exist, is to create a subuser, if not, is to create a subprofile group
        create_subuser = request.POST.get("first_name", False)
        if create_subuser:
            form = RegisterSubuser(request.POST, request.FILES, user_pk=request.user.pk)
            if not form.is_valid():
                return render(
                    request,
                    "Users/subusers.html",
                    {
                        "form": form,
                        "group_form": RegisterSubprofileGroup(),
                        "checked": "checked",
                        "subusers": subusers,
                        "profile": profile,
                        "type": "profile",
                        "permissions": permissions,
                    },
                )
            subuser = form.save(commit=False)
            subuser.username = subuser.first_name + subuser.last_name
            subuser.save()
            form.create_subprofile(
                user=subuser,
                group_id=request.POST["group"],
                image=request.FILES.get("image", "default.jpg"),
            )

            UserChanges.objects.create(
                main_user=subuser.subprofile.profile.user,
                user_changed=subuser,
                user=request.user,
                description=f'Se creó el usuario "{subuser.first_name} {subuser.last_name}" perteneciente al grupo "{subuser.subprofile.group.name}"',
                type_change=TypeChanges.objects.get(value="Create")
                )
            # SEND EMAIL
            current_site = get_current_site(request)
            subject = "Bienvenido a Log Inventory"
            link = f"http://{current_site.domain}"
            message = render_to_string(
                "notification_email.html",
                {
                    "user": subuser,
                    'link' : link,
                    'main_account' : profile_admin.user.username                    
                },
            )
            send_mail(
                subject,
                message,
                None,
                [subuser.email],
                fail_silently=False,
            )
            messages.success(request, "El usuario se creó con éxito.")
            return redirect("manage_subusers")
        else:
            form = RegisterSubprofileGroup(
                request.POST, request.FILES, user_pk=request.user.pk
            )
            if not form.is_valid():
                return render(
                    request,
                    "Users/subprofiles_group.html",
                    {
                        "form": RegisterSubuser(user_pk=request.user.pk),
                        "group_form": form,
                        "checked_group": "checked",
                        "subusers": subusers,
                        "profile": profile,
                        "type": "profile",
                        "permissions": permissions,
                    },
                )
            form.create_subprofile_group(
                image=request.FILES.get("image", "default_group.jpg")
            )
            messages.success(request, "El grupo se creó con éxito.")
            return redirect("subusers_group")


@login_required
def subprofile(request, id):
    # verifie that exist one user with this name
    try:
        subuser = User.objects.get(id=id)
    except:
        messages.error(request, "El usuario no existe.")
        return redirect("authenticate", type="deactivate")
    # Get user
    user = request.user
    if subuser != user:
        try:
            # get subprofile from the subuser
            subprofile = Subprofile.objects.get(user=subuser)
            subuser_pk = subuser.pk
        except ObjectDoesNotExist:
            messages.error(request, "El usuario no existe.")
            return redirect("main")
        # try get profile from the user, if raise a exception in the next try
        try:
            profile = user.profile
            type = "profile"
            permissions = "admin"
            if subprofile.profile != profile:
                logout(request)
                messages.warning(
                    request,
                    "No tienes permiso para ver información acerca de ese usuario.",
                )
                return redirect("authenticate", type="deactivate")
        except ObjectDoesNotExist:
            profile = Subprofile.objects.get(user=user)
            type = "subprofile"
            permissions = profile.group.permissions.name
            if subprofile.profile != profile.profile:
                logout(request)
                messages.warning(
                    request,
                    "No tienes permiso para ver información acerca de ese usuario.",
                )
                return redirect("authenticate", type="deactivate")
            if permissions == "Estudiante":
                messages.warning(
                    request, "No tienes permiso para ver información de otros usuarios."
                )
                return redirect("authenticate", type="deactivate")
        except:
            messages.error(request, "El usuario no existe.")
            return redirect("main")
    else:
        subprofile = Subprofile.objects.get(user=subuser)
        subuser_pk = subuser.pk
        permissions = subprofile.group.permissions.name
        type = "subprofile"
        profile = user.subprofile
    form = EditSubprofileForm(
        instance=subuser, user_pk=subuser_pk, permissions=permissions
    )
    if request.method == "GET":
        return render(
            request,
            "Users/subprofile.html",
            {
                "subprofile": subprofile,
                "profile": profile,
                "form": form,
                "image_form": SetImageForm(),
                "type": type,
                "permissions": permissions,
                "password_form": SetPassword(user=subuser),
            },
        )
    else:
        if request.POST.get("delete_subprofile", False):
            if permissions != "admin":
                messages.error(request, "No tienes permiso para eliminar este usuario.")
                return redirect("subprofile", id=id)
            if subprofile.profile.user == subuser:
                messages.error(
                    request, "No puedes eliminar el usuario principal de la cuenta."
                )
                return redirect("subprofile", id=id)
            if (
                Objects.objects.filter(in_charge=subprofile, is_active=True).exists()
                or ObjectsGroup.objects.filter(
                    in_charge=subprofile, is_active=True
                ).exists
            ):
                messages.error(
                    request,
                    "No se puede eliminar el usuario porque tiene objetos o grupos de objetos a cargo. Cambia el encargado de esos objetos e inténtalo de nuevo.",
                )
                return redirect("subprofile", id=id)
            
            subprofile.is_active = False
            subprofile.save()
            subuser.is_active = False
            subuser.save()
            
            messages.success(request, "El usuario se eliminó con éxito.")
            return redirect("manage_subusers")

        image = request.FILES.get("image", False)
        delete_image = request.POST.get("delete_image", False)
        change_password = request.POST.get("new_password2", "")
        if change_password == "":
            change_password = False
        if image:
            image_before = subprofile.image.name
            if image_before == "default.jpg":
                image_before = "Ninguna"
            subprofile.image = image
            subprofile.save()
            log = TypeChanges.objects.get(value="Update")
            UserChanges.objects.create(
                main_user=subprofile.profile.user,
                user_changed=subprofile.user,
                user=request.user,
                description=f"Cambio en imagen, antes: {image_before}, después: {image}",
                type_change=log,
            )
            messages.success(request, "La iamgen se cambió con éxito.")
            return redirect("subprofile", id=id)
        elif delete_image:
            image_before = subprofile.image.name
            if image_before == "default.jpg":

                messages.error(
                    request,
                    "La imagen no se puedo borrar ya que el usuario no tiene una image relacionada.",
                )
                return redirect("subprofile", id=id)
            subprofile.image = "default.jpg"
            subprofile.save()
            log = TypeChanges.objects.get(value="Update")
            UserChanges.objects.create(
                main_user=subprofile.profile.user,
                user_changed=subprofile.user,
                user=request.user,
                description=f'Cambio en imagen, antes: "{image_before}", despúes: "Ninguna"',
                type_change=log,
            )
            messages.success(request, "La imagen se borró con éxito.")
            return redirect("subprofile", id=id)
        else:

            form_post = EditSubprofileForm(
                request.POST,
                initial=form.initial,
                instance=subuser,
                user_pk=subuser_pk,
                permissions=permissions,
            )
            data = form_post.data

            if not form_post.has_changed() and change_password == False:
                messages.warning(request, "Los datos no han sido actualizados.")
                return redirect("subprofile", id=id)
            if change_password:
                password_form = SetPassword(user=subuser, data=request.POST)
                if not password_form.is_valid():
                    messages.warning(
                        request,
                        "Hubo un error al cambiar la contraseña, todos los demás posibles datos ingresados no se guardarán.",
                    )
                    return render(
                        request,
                        "Users/subprofile.html",
                        {
                            "subprofile": subprofile,
                            "profile": profile,
                            "form": form,
                            "form_post": form_post,
                            "image_form": SetImageForm(),
                            "type": type,
                            "permissions": permissions,
                            "password_form": password_form,
                        },
                    )
                password_form.save()
                log = TypeChanges.objects.get(value="Update")
                UserChanges.objects.create(
                    main_user=subprofile.profile.user,
                    user_changed=subuser,
                    user=request.user,
                    description=f"Se cambió la contraseña.",
                    type_change=log,
                )
                messages.success(request, "La contraseña se cambió con exito.")
            if not form_post.is_valid():
                return render(
                    request,
                    "Users/subprofile.html",
                    {
                        "subprofile": subprofile,
                        "profile": profile,
                        "form": form,
                        "form_post": form_post,
                        "image_form": SetImageForm(),
                        "type": type,
                        "permissions": permissions,
                        "password_form": SetPassword(user=subuser),
                    },
                )

            user = User.objects.get(pk=subuser_pk)
            User.objects.filter(pk=subuser_pk).update(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
            )
            try:
                Subprofile.objects.filter(user=user).update(group=data["group"])
            except:
                pass
            messages.success(request, "Los datos se actualizaron con éxito.")
            if permissions == "admin" or permissions == "Profesor":
                return redirect("manage_subusers")
            else:
                return redirect("main")


@login_required
def manage_subusers_group(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        profile_admin = profile
        user_pk = user.pk
        type = "profile"
        permissions = "admin"
    except ObjectDoesNotExist:
        profile = Subprofile.objects.get(user=user)
        profile_admin = profile.profile
        user_pk = profile.profile.user.pk
        type = "subprofile"
        permissions = profile.group.permissions.name
        if permissions == "Estudiante":
            messages.warning(request, "No tienes permiso para ver esa página.")
            return redirect("authenticate", type="deactivate")
    except:
        messages.error(request, "Hubo un error al tratar de cargar los grupos.")
        return redirect("authenticate", type="deactivate")
    query_subgroups = SubprofilesGroup.objects.filter(
        profile=profile_admin, is_active=True
    )
    forms = []
    for group in query_subgroups:
        form = EditSubprofileGroupForm(instance=group, user_pk=user_pk)
        forms.append(form)
    if request.method == "GET":
        return render(
            request,
            "Users/subprofiles_group.html",
            {
                "type": type,
                "profile": profile,
                "permissions": permissions,
                "forms": forms,
                "image_form": SetImageForm(),
                "groups": query_subgroups,
                "subuser_form": RegisterSubuser(user_pk=request.user.pk),
                "group_form": RegisterSubprofileGroup(),
            },
        )
    else:
        image = request.FILES.get("image", False)
        delete_image = request.POST.get("delete_image", False)
        delete_group = request.POST.get("delete_group", False)
        if delete_group:
            group = SubprofilesGroup.objects.get(pk=request.POST["id"])
            subprofiles = Subprofile.objects.filter(group=group)
            if subprofiles.count() > 0:
                messages.error(
                    request,
                    "No se puede eliminar el grupo porque tiene usuarios asociados.",
                )
                return render(
                    request,
                    "Users/subprofiles_group.html",
                    {
                        "type": type,
                        "profile": profile,
                        "permissions": permissions,
                        "forms": forms,
                        "image_form": SetImageForm(),
                        "groups": query_subgroups,
                        "subuser_form": RegisterSubuser(user_pk=request.user.pk),
                        "group_form": RegisterSubprofileGroup(),
                    },
                )
            group.is_active = False
            group.save()
            messages.success(request, "El grupo se borró con éxito.")
            return redirect("subusers_group")
        elif image:
            group = SubprofilesGroup.objects.get(pk=request.POST["id"])
            image_before = group.image.name
            if image_before == "default_group.jpg":
                image_before = "Ninguna"
            group.image = image
            group.save()
            log = TypeChanges.objects.get(value="Update")
            GroupChanges.objects.create(
                main_user=group.profile.user,
                group_changed=group,
                user=request.user,
                description=f"Cambio en imagen, antes: {image_before}, después: {image}",
                type_change=log,
            )
            messages.success(request, "La imagen se cambió con éxito.")
            return redirect("subusers_group")
        elif delete_image:
            group = SubprofilesGroup.objects.get(pk=request.POST["id"])
            image_before = group.image.name
            if image_before == "default_group.jpg":
                messages.error(
                    request,
                    f"No se puede borrar la imagen del grupo {group.name} porque no tiene imagen.",
                )
                return redirect("subusers_group")
            group.image = "default_group.jpg"
            group.save()
            log = TypeChanges.objects.get(value="Update")
            GroupChanges.objects.create(
                main_user=group.profile.user,
                group_changed=group,
                user=request.user,
                description=f'Cambio en imagen, antes: "{image_before}", después: "Ninguna"',
                type_change=log,
            )
            messages.success(request, "La imagen se borró con éxito.")
            return redirect("subusers_group")
        
        else:
            group = SubprofilesGroup.objects.get(pk=request.POST["id"])
            form = EditSubprofileGroupForm(instance=group, user_pk=user_pk)
            form_post = EditSubprofileGroupForm(
                request.POST, instance=group, user_pk=user_pk
            )
            if (
                request.POST["name"] == group.name
                and request.POST["permissions"] == str(group.permissions.pk)
                and request.POST["description"] == group.description
            ):
                messages.warning(request, "Los datos no han sido actualizados.")
                return render(
                    request,
                    "Users/subprofiles_group.html",
                    {
                        "type": type,
                        "profile": profile,
                        "permissions": permissions,
                        "forms": forms,
                        "form_post": form_post,
                        "group": group,
                        "image_form": SetImageForm(),
                        "groups": query_subgroups,
                        "subuser_form": RegisterSubuser(user_pk=request.user.pk),
                        "group_form": RegisterSubprofileGroup(),
                    },
                )
            if not form_post.is_valid():
                return render(
                    request,
                    "Users/subprofiles_group.html",
                    {
                        "type": type,
                        "profile": profile,
                        "permissions": permissions,
                        "forms": forms,
                        "form_post": form_post,
                        "group": group,
                        "image_form": SetImageForm(),
                        "groups": query_subgroups,
                        "subuser_form": RegisterSubuser(user_pk=request.user.pk),
                        "group_form": RegisterSubprofileGroup(),
                    },
                )
            form_post.save()
            messages.success(request, "Los datos se actualizaron con éxito.")
            return redirect("subusers_group")
