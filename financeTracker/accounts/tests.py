from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Importing the specific profile models
from .models import UserProfile, AdminUserProfile, RegUserProfile

User = get_user_model()

class UserTestCase(TestCase):
    """
    Test case for the User model and related functionality.
    """

    def setUp(self):
        """
        Set up function to create a user for testing.
        """
        # Creating a regular user for testing
        self.user = get_user_model().objects.create_user(
            email="test@test.com", first_name="Test", last_name="User", password="test12345", role=User.Role.REG_USER
        )

    def test_user_creation(self):
        """
        Test the creation of a user.
        """
        self.assertEqual(self.user.email, "test@test.com")
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertTrue(self.user.is_active)

    def test_profile_creation(self):
        """
        Test automatic creation of user profile.
        """
        # Adjust the test to reflect the correct profile type
        profile = None
        if self.user.role == User.Role.ADMIN:
            profile = AdminUserProfile.objects.filter(user=self.user).first()
        elif self.user.role == User.Role.REG_USER:
            profile = RegUserProfile.objects.filter(user=self.user).first()
        else:
            profile = UserProfile.objects.filter(user=self.user).first()

        self.assertIsNotNone(profile)

class UserViewTestCase(TestCase):
    """
    Test case for user-related views.
    """

    def setUp(self):
        """
        Set up function to create a user and log them in for testing.
        """
        self.user = get_user_model().objects.create_user(
            email="viewtest@test.com", first_name="ViewTest", last_name="User", password="viewtest12345",
            role=User.Role.REG_USER
        )
        self.client.login(email="viewtest@test.com", password="viewtest12345")

    def test_dashboard_access(self):
        """
        Test access to the user dashboard.
        """
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')

    def test_logout_redirect(self):
        """
        Test logout functionality and redirect.
        """
        # Ensure the user is logged in
        self.assertTrue(self.client.session['_auth_user_id'], "User is not logged in for testing.")

        # Attempt to logout and follow the redirect
        response = self.client.get(reverse('logout'), follow=True)

        # Debugging information
        print("Logout Response Status Code:", response.status_code)
        print("Logout Response Content:", response.content)

        # Check if the final response is the login page
        self.assertRedirects(response, reverse('login'))
