from django.urls import path
from .views import home, authenticate, main,Logout
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from Users.forms import PasswordReset, SetPassword

urlpatterns = [
    path('', home, name='home'),
    path('authenticate_user/', authenticate, name='authenticate'),
    path('work_space/', main, name='main'),
    path('logout/', Logout, name='logout'),
    path('reset/', PasswordResetView.as_view(template_name = 'Users/password_reset.html', form_class = PasswordReset), name='password_reset'),
    path('reset_done/', PasswordResetDoneView.as_view(template_name = 'Users/password_reset_done.html'), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>',  PasswordResetConfirmView.as_view(template_name = 'Users/password_reset_confirm.html',form_class = SetPassword), name = 'password_reset_confirm'),
    path('reset_complete/', PasswordResetCompleteView.as_view(template_name = 'Users/password_reset_complete.html'), name = 'password_reset_complete'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)