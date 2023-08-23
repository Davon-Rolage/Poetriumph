from django.urls import path

from .views import LoginView, MyProfileView, SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('my-profile/', MyProfileView.as_view(), name='my_profile'),
]
