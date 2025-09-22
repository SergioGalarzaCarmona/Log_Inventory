from django.urls import path
from .views import home, authenticate_user, Logout, profile, manage_subusers, subprofile, manage_subusers_group, UserPasswordChangeView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeDoneView
from Users.forms import PasswordReset, SetPassword

urlpatterns = [
    path('', home, name='home'),
    path('authenticate_user/<str:type>', authenticate_user, name='authenticate'),
    path('logout/', Logout, name='logout'),
    path('reset/', PasswordResetView.as_view(template_name = 'Users/password_reset.html', form_class = PasswordReset), name='password_reset'),
    path('reset_done/', PasswordResetDoneView.as_view(template_name = 'Users/password_reset_done.html'), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>',  PasswordResetConfirmView.as_view(template_name = 'Users/password_reset_confirm.html',form_class = SetPassword), name = 'password_reset_confirm'),
    path('reset_complete/', PasswordResetCompleteView.as_view(template_name = 'Users/password_reset_complete.html'), name = 'password_reset_complete'),
    path('change_password/', UserPasswordChangeView.as_view(template_name = 'Users/change_password.html', form_class = SetPassword), name='change_password'),
    path('change_password_done/', PasswordChangeDoneView.as_view(template_name = 'Users/password_reset_complete.html'), name='change_password_done'),
    path('profile/<int:id>', profile, name='profile'),
    path('manage_subusers/',manage_subusers, name='manage_subusers'),
    path('subprofile/<int:id>',subprofile, name='subprofile'),
    path('subusers_group/',manage_subusers_group,name='subusers_group'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
