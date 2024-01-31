from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import UserRegistrationForm


# This section defines views related to user authentication, registration, and dashboard access.

# View for user registration.
class UserRegistrationView(SuccessMessageMixin, CreateView):
    # Specifies the template to use for the registration page.
    template_name = "accounts/register.html"
    # Specifies the form class for user registration.
    form_class = UserRegistrationForm
    # URL to redirect to after successful registration.
    success_url = reverse_lazy("login")
    # Success message to display after successful registration.
    success_message = "Hi %(first_name)s, Your account has been created! You are now able to log in"

    # Method to handle valid form submission.
    def form_valid(self, form):
        response = super().form_valid(form)
        # Display success message with user's first name.
        messages.success(
            self.request,
            self.success_message % {"first_name": form.cleaned_data["first_name"]},
        )
        return response


# View for user login.
class UserLoginView(LoginView):
    # Specifies the template to use for the login page.
    template_name = "accounts/login.html"
    # URL to redirect to after successful login.
    success_url = reverse_lazy("dashboard")


# View for user logout.
class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        # Render the custom logout template
        response = render(request, "accounts/logout.html")

        # Perform the logout action
        logout(request)

        # After rendering the logout template, redirect to the login page
        return redirect('login')


# View for the user dashboard.
@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
class UserDashboardView(TemplateView):
    # Specifies the template to use for the dashboard page.
    template_name = 'accounts/dashboard.html'

    # Method to add additional context to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Check if the user has admin or regular user profile and add this info to the context.
        context['has_admin_profile'] = hasattr(user, 'adminuserprofile')
        context['has_reg_profile'] = hasattr(user, 'reguserprofile')
        return context

# The views defined here follow Django's class-based views pattern, which is recommended for handling web pages
# with complex functionalities. This pattern promotes reusability and maintainability of code, which is essential
# in large tech environments. The use of decorators and mixins enhances functionality without cluttering the
# core view logic.
