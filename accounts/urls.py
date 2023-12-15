from django.urls import path

from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate_user/<str:token>/', ActivateUserView.as_view(), name='activate_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),
    path('check-username-exists/', check_username_exists, name='check_username_exists'),
    path('premium/', PremiumView.as_view(), name='premium'),
    path('get-premium/', GetPremiumView.as_view(), name='get_premium'),
    path('cancel-premium/', CancelPremiumView.as_view(), name='cancel_premium'),
]
