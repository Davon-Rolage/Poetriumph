from django.urls import path

from .views import *


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('check-username-exists/', check_username_exists, name='check_username_exists'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    path('activate_user/<str:token>/', ActivateUserView.as_view(), name='activate_user'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-check/<str:token>/', PasswordResetCheckView.as_view(), name='password_reset_check'),
    path('set-password/<str:token>/', SetPasswordView.as_view(), name='set_password'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/deactivate/', DeactivateUserView.as_view(), name='deactivate_user'),
    path('premium/', PremiumView.as_view(), name='premium'),
    path('get-premium/', GetPremiumView.as_view(), name='get_premium'),
    path('cancel-premium/', CancelPremiumView.as_view(), name='cancel_premium'),
]
