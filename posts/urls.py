from django.urls import path

from . import views


app_name = "posts"

urlpatterns = [
    path("", views.PostFeedView.as_view(), name="feed"),
    path("new/", views.PostCreateView.as_view(), name="create"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.PostUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.post_delete_view, name="delete"),
    path("<int:pk>/like/", views.post_like_view, name="like"),
    path("<int:pk>/unlike/", views.post_unlike_view, name="unlike"),
    path("<int:pk>/save/", views.post_save_view, name="save"),
    path("<int:pk>/unsave/", views.post_unsave_view, name="unsave"),
    path("<int:pk>/comment/", views.post_comment_view, name="comment"),
    path("<int:pk>/comment/<int:comment_id>/like/", views.post_like_comment_view, name="like_comment"),
    path("<int:pk>/comment/<int:comment_id>/unlike/", views.post_unlike_comment_view, name="unlike_comment"),
    path("<int:pk>/comment/<int:comment_id>/delete/", views.post_delete_comment_view, name="delete_comment"),
]
