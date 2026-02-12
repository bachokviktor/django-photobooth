from django.urls import path

from . import views


app_name = "posts"

urlpatterns = [
    path("", views.PostFeedView.as_view(), name="feed"),
    path("new/", views.PostCreateView.as_view(), name="create"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.PostUpdateView.as_view(), name="edit"),
    path("<int:pk>/like/", views.post_like_view, name="like"),
    path("<int:pk>/unlike/", views.post_unlike_view, name="unlike"),
    path("<int:pk>/save/", views.post_save_view, name="save"),
    path("<int:pk>/unsave/", views.post_unsave_view, name="unsave"),
]
