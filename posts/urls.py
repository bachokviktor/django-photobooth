from django.urls import path

from . import views


app_name = "posts"

urlpatterns = [
    path("", views.empty, name="home"),
    path("p/new/", views.PostCreateView.as_view(), name="create"),
]
