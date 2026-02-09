from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import View, generic
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms


# Create your views here.
class UserProfileRedirectView(LoginRequiredMixin, View):
    """
    This view redirects the user to his profile if he is
    authenticated, and to the login page if not.
    """
    login_url = reverse_lazy("users:login")

    def get(self, request):
        return redirect("users:profile", username=request.user.username)


class UserProfileView(generic.DetailView):
    """
    This view displays profile of a user.
    """
    model = get_user_model()
    template_name = "users/profile.html"
    context_object_name = "profile_user"

    def get_object(self):
        username = self.kwargs["username"]

        obj = get_object_or_404(self.model, username=username)

        return obj


class UserRegisterView(View):
    """
    This view handles user registration.
    """
    form_class = forms.CustomUserCreationForm
    template_name = "users/register.html"

    def get(self, request):
        form = self.form_class()

        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("users:profile", username=user.username)

        return render(request, self.template_name, {"form": form})


class UserLoginView(View):
    """
    This view handles user authentication.
    """
    form_class = AuthenticationForm
    template_name = "users/login.html"

    def get(self, request):
        form = self.form_class()

        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_page = request.POST["next"]
            if next_page:
                return redirect(next_page)

            return redirect("users:profile", username=user.username)

        return render(request, self.template_name, {"form": form})


class UserEditProfileView(LoginRequiredMixin, View):
    """
    This view allows an authenticated user to edit
    his profile.
    """
    login_url = reverse_lazy("users:login")
    form_class = forms.UserEditProfileForm
    template_name = "users/edit_profile.html"

    def get(self, request):
        form = self.form_class(instance=request.user)

        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()

            return redirect("users:profile", username=request.user.username)

        return render(request, self.template_name, {"form": form})


def user_logout_view(request):
    """
    This view handles user logout.
    Does not require user to be authenticated.
    """
    logout(request)

    return redirect("users:login")


@login_required(login_url=reverse_lazy("users:login"))
def user_follow_view(request, username):
    """
    This view allows an authenticated user to follow other users.
    """
    if request.method == "POST":
        user = get_object_or_404(get_user_model(), username=username)

        request.user.follow(user)

    return redirect("users:profile", username=username)


@login_required(login_url=reverse_lazy("users:login"))
def user_unfollow_view(request, username):
    """
    This view allows an authenticated user to unfollow other users.
    """
    if request.method == "POST":
        user = get_object_or_404(get_user_model(), username=username)

        request.user.unfollow(user)

    return redirect("users:profile", username=username)


@login_required(login_url=reverse_lazy("users:login"))
def user_remove_follower_view(request, username):
    """
    This view allows an authenticated user to remove his followers.
    """
    if request.method == "POST":
        user = get_object_or_404(get_user_model(), username=username)

        request.user.remove_follower(user)

    return redirect("users:profile", username=username)
