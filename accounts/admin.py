from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .forms import *
from .models import *


class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = UserChangeForm
    model = get_user_model()
    list_display = ['username', 'email', 'is_premium', 'date_joined', 'is_active']
    list_filter = ['is_premium', 'is_active', 'date_joined']
    sortable_by = ['username', 'is_premium', 'date_joined']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_premium',)}),
    )


class CustomUserTokenAdmin(admin.ModelAdmin):
    model = CustomUserToken
    ordering = ('-expire_date',)
    list_display = ['user', 'token_type', 'expire_date', 'token']
    list_display_links = ['user', 'token']
    list_filter = ['token_type', 'expire_date', 'user']
    sortable_by = ['user', 'token_type', 'expire_date']


class CustomUserTokenTypeAdmin(admin.ModelAdmin):
    model = CustomUserTokenType
    ordering = ('id',)
    list_display = ['name', 'id']
    list_display_links = ['name', 'id']


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user', 'total_poems']
    list_filter = ['user__is_premium']


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(CustomUserToken, CustomUserTokenAdmin)
admin.site.register(CustomUserTokenType, CustomUserTokenTypeAdmin)
admin.site.register(Profile, ProfileAdmin)
