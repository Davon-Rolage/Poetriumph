from django.urls import path

from .views import SignUpView, LoginView, MyProfileView, DeleteUserView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('my-profile/', MyProfileView.as_view(), name='my_profile'),
    path('my-profile/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),
]
