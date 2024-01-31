from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import (
    User,
    AdminUser,
    RegUser,
    UserProfile,
    AdminUserProfile,
    RegUserProfile,
)


# Define an inline admin for the UserProfile model
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


# Define an inline admin for each proxy profile
class AdminUserProfileInline(admin.StackedInline):
    model = AdminUserProfile
    can_delete = False


class RegUserProfileInline(admin.StackedInline):
    model = RegUserProfile
    can_delete = False


# Define a custom UserAdmin to include the UserProfileInline
class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
        ("Custom fields", {"fields": ("role",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "role",
                ),
            },
        ),
    )

    ordering = ("email",)

    list_display = ("first_name", "last_name", "email", "is_staff", "is_active", "role")


# Define a custom AdminUserAdmin to include the AdminUserProfileInline
class AdminUserAdmin(CustomUserAdmin):
    inlines = [AdminUserProfileInline]


# Define a custom RegUserAdmin to include the RegUserProfileInline
class RegUserAdmin(CustomUserAdmin):
    inlines = [RegUserProfileInline]


# Register the base User model with the custom admin class
admin.site.register(User, CustomUserAdmin)

# Register the proxy models with the custom admin classes
admin.site.register(AdminUser, AdminUserAdmin)
admin.site.register(RegUser, RegUserAdmin)

# Register the profile models with their respective admin classes
admin.site.register(UserProfile)
admin.site.register(AdminUserProfile)
admin.site.register(RegUserProfile)

# Unregister the Group model
admin.site.unregister(Group)
