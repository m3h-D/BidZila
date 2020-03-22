from django.urls import path
from .views import(
    login_view,
    register_view,
    logout_view,
    profile_edit,
    profile,
    change_password_view,
    wallet,
)
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView


urlpatterns = [
    path('login/', login_view, name='login-view'),
    path('register/', register_view, name='register-view'),
    path('logout/', logout_view, name='logout-view'),
    path('profile/', profile, name='profile-view'),
    path('wallet/', wallet, name='wallet'),
    path('profile/edit/', profile_edit, name='edit-profile-view'),
    path('profile/edit-fbv/', profile_edit, name='edit-profile-view-action'),
    path('change-password/', change_password_view, name='change-password'),


    path('password-reset/', PasswordResetView.as_view(
        template_name='accounts/password_reset.html'), name='password_reset'),

    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete')
]
