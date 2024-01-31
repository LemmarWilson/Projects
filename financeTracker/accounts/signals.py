from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, AdminUserProfile, RegUserProfile, UserProfile

# Django signals are used here to automate the creation and updating of user profiles.
# Signals allow certain actions to occur in response to model changes.

# Signal receiver for creating user profiles.
# This method is triggered after a User model instance is saved for the first time.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Check if this is a new instance of User.
    if created:
        # Depending on the user's role, create the corresponding profile type.
        if instance.role == User.Role.ADMIN:
            # Create an AdminUserProfile if the user is an admin.
            AdminUserProfile.objects.get_or_create(user=instance)
        elif instance.role == User.Role.REG_USER:
            # Create a RegUserProfile if the user is a regular user.
            RegUserProfile.objects.get_or_create(user=instance)
        else:
            # For any other role, create a generic UserProfile.
            UserProfile.objects.get_or_create(user=instance)

# Signal receiver for saving user profiles.
# This method is triggered each time a User model instance is saved.
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Check if the user instance has an associated adminuserprofile and save it if present.
    if hasattr(instance, 'adminuserprofile'):
        instance.adminuserprofile.save()
    # Check if the user instance has an associated reguserprofile and save it if present.
    elif hasattr(instance, 'reguserprofile'):
        instance.reguserprofile.save()
    # For any other user, save the associated generic user profile.
    # Note: The 'user_profile' related name should match the related_name in the OneToOneField of UserProfile.
    elif hasattr(instance, 'user_profile'):
        instance.user_profile.save()

# These signals help in maintaining data integrity and automate the process of profile creation and updates.
# They are a part of Django's robust framework for handling database operations triggered by model changes.
