from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, CustomUserToken, Profile


class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'is_premium', 'date_joined']
    list_filter = ['is_premium', 'date_joined']
    sortable_by = ['username', 'is_premium', 'date_joined']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_premium',)}),
    )
    
    
class CustomUserTokenAdmin(admin.ModelAdmin):
    model = CustomUserToken
    list_display = ['user', 'token', 'expire_date']
    list_filter = ['user', 'expire_date']
    sortable_by = ['user', 'token', 'expire_date']


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user', 'total_poems']
    list_filter = ['user__is_premium']
    sortable_by = ['user']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomUserToken, CustomUserTokenAdmin)
admin.site.register(Profile, ProfileAdmin)
