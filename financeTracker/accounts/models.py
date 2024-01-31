from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, Group,
)


# This section creates custom user models and related profiles, following best practices in modern web development.

# Custom manager for the User model. This is used to define helper methods for creating users and superusers.
class UserManager(BaseUserManager):

    # Helper function for creating a user. It's a private method, as indicated by the underscore prefix.
    def _create_user(self, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("Password is required")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Public method to create a regular user.
    def create_user(self, email=None, first_name=None, last_name=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", User.Role.REG_USER)
        return self._create_user(email, first_name, last_name, password, **extra_fields)

    # Public method to create a superuser.
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)

        user = self._create_user(email, first_name, last_name, password, **extra_fields)
        admin_group, created = Group.objects.get_or_create(name='Admins')
        user.groups.add(admin_group)

        user.save(using=self._db)
        return user


# Custom User model, inheriting from AbstractBaseUser and PermissionsMixin.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=250)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)

    groups = models.ManyToManyField(Group, verbose_name="groups", blank=True, related_name="custom_user_set")
    user_permissions = models.ManyToManyField(Permission, verbose_name="user permissions", blank=True,
                                              related_name="custom_user_set")

    objects = UserManager()

    # Establishing a OneToOne relationship with UserProfile. 'related_name' is used for reverse querying.
    profile = models.OneToOneField("accounts.UserProfile", on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="user_profile")

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    # Enumeration for user roles.
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        REG_USER = "USER", "User"

    role = models.CharField(max_length=50, choices=Role.choices)

    # Overriding the save method to handle the creation of a user profile when a new user is created.
    def save(self, *args, **kwargs):
        user_is_new = self._state.adding
        super().save(*args, **kwargs)
        if user_is_new:
            if self.role == User.Role.ADMIN:
                AdminUserProfile.objects.get_or_create(user=self)
            elif self.role == User.Role.REG_USER:
                RegUserProfile.objects.get_or_create(user=self)
            else:
                UserProfile.objects.get_or_create(user=self)

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name


# Base model for user profiles.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')

    def __str__(self):
        return self.user.first_name


# ========== Proxy Models ==========

# Proxy models are used here to create specific types of users. They don't create a new table in the database but extend the User model.

# Custom manager for AdminUser model.
class AdminUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.ADMIN)


# AdminUser proxy model.
class AdminUser(User):
    objects = AdminUserManager()

    class Meta:
        proxy = True
        verbose_name = "Admin User"
        verbose_name_plural = "Admin Users"


# Custom manager for RegUser model.
class RegUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.REG_USER)


# RegUser proxy model.
class RegUser(User):
    objects = RegUserManager()

    class Meta:
        proxy = True
        verbose_name = "Regular User"
        verbose_name_plural = "Regular Users"


# ========== Profile Proxy Models ==========

# These models are used to extend the UserProfile with additional fields specific to the user type.

# AdminUserProfile model for admin users.
class AdminUserProfile(UserProfile):
    bio = models.TextField(blank=True, null=True)
    age = models.IntegerField(null=True, blank=True, default=6)

    class Meta:
        verbose_name = 'Admin User Profile'
        verbose_name_plural = 'Admin User Profiles'


# RegUserProfile model for regular users.
class RegUserProfile(UserProfile):
    bio = models.TextField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        verbose_name = 'Regular User Profile'
        verbose_name_plural = 'Regular User Profiles'
