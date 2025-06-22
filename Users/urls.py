from django.urls import path
from .views import home, authenticate_user, main, Logout, profile, manage_subusers, subprofile, manage_subusers_group, log_users
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from Users.forms import PasswordReset, SetPassword

urlpatterns = [
    path('', home, name='home'),
    path('authenticate_user/<str:type>', authenticate_user, name='authenticate'),
    path('logout/', Logout, name='logout'),
    path('reset/', PasswordResetView.as_view(template_name = 'Users/password_reset.html', form_class = PasswordReset), name='password_reset'),
    path('reset_done/', PasswordResetDoneView.as_view(template_name = 'Users/password_reset_done.html'), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>',  PasswordResetConfirmView.as_view(template_name = 'Users/password_reset_confirm.html',form_class = SetPassword), name = 'password_reset_confirm'),
    path('reset_complete/', PasswordResetCompleteView.as_view(template_name = 'Users/password_reset_complete.html'), name = 'password_reset_complete'),
    path('change_password/', PasswordChangeView.as_view(template_name = 'Users/change_password.html', form_class = SetPassword, success_url='/authenticate_user/deacticate'), name='change_password'),
    path('change_password_done/', PasswordChangeDoneView.as_view(template_name = 'Users/password_reset_complete.html'), name='change_password_done'),
    path('work_space/', main, name='main'),
    path('profile/<str:username>', profile, name='profile'),
    path('manage_subusers/',manage_subusers, name='manage_subusers'),
    path('subprofile/<str:username>',subprofile, name='subprofile'),
    path('subusers_group/',manage_subusers_group,name='subusers_group'),
    path('user_log/',log_users, name='user_log'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
