from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path("", views.UserProfileRedirectView.as_view(), name="profile_redirect"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("edit-profile/", views.UserEditProfileView.as_view(), name="edit_profile"),
    path("logout/", views.user_logout_view, name="logout"),
    path("<str:username>/", views.UserProfileView.as_view(), name="profile"),
    path("<str:username>/follow/", views.user_follow_view, name="follow"),
    path("<str:username>/unfollow/", views.user_unfollow_view, name="unfollow"),
    path("<str:username>/remove-follower/", views.user_remove_follower_view, name="remove_follower"),
]
