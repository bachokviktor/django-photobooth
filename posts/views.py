from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from . import models, forms


# Create your views here.
def empty(request, *args, **kwargs):
    return HttpResponse("<h2>Empty page</h2>")

class PostFeedView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy("users:login")
    template_name = "posts/feed.html"
    queryset = models.Post.objects.all().order_by("-created_at")
    context_object_name = "posts"


class PostDetailView(generic.DetailView):
    model = models.Post
    template_name = "posts/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["comment_form"] = forms.CommentForm()

        return context


class PostCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:login")
    form_class = forms.PostForm
    template_name = "posts/create.html"

    def get(self, request):
        form = self.form_class()

        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()

            for photo in request.FILES.getlist("post_photos"):
                models.PostPhoto.objects.create(photo=photo, post=instance)

            return redirect("posts:feed")

        return render(request, self.template_name, {"form": form})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy("users:login")
    form_class = forms.PostUpdateForm
    template_name = "posts/edit.html"

    def test_func(self, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=self.kwargs["pk"])
        
        return self.request.user == post.author

    def get(self, request, pk):
        post = get_object_or_404(models.Post, pk=pk)
        form = self.form_class(instance=post)

        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        post = get_object_or_404(models.Post, pk=pk)
        form = self.form_class(request.POST, request.FILES, instance=post)

        if form.is_valid():
            instance = form.save()

            for photo in request.FILES.getlist("new_photos"):
                models.PostPhoto.objects.create(photo=photo, post=instance)

            return redirect("posts:detail", pk=pk)

        return render(request, self.template_name, {"form": form})


@login_required(login_url=reverse_lazy("users:login"))
def post_delete_view(request, pk):
    if request.method == "POST":
        post = get_object_or_404(models.Post, pk=pk)

        if request.user == post.author:
            post.delete()

    return redirect("posts:feed")


@login_required(login_url=reverse_lazy("users:login"))
def post_like_view(request, pk):
    if request.method == "POST":
        post = get_object_or_404(models.Post, pk=pk)

        if request.user not in post.likes.all():
            post.likes.add(request.user)

    return redirect("posts:detail", pk=pk)


@login_required(login_url=reverse_lazy("users:login"))
def post_unlike_view(request, pk):
    if request.method == "POST":
        post = get_object_or_404(models.Post, pk=pk)

        if request.user in post.likes.all():
            post.likes.remove(request.user)

    return redirect("posts:detail", pk=pk)


@login_required(login_url=reverse_lazy("users:login"))
def post_save_view(request, pk):
    if request.method == "POST":
        post = get_object_or_404(models.Post, pk=pk)

        if request.user not in post.saves.all():
            post.saves.add(request.user)

    return redirect("posts:detail", pk=pk)


@login_required(login_url=reverse_lazy("users:login"))
def post_unsave_view(request, pk):
    if request.method == "POST":
        post = get_object_or_404(models.Post, pk=pk)

        if request.user in post.saves.all():
            post.saves.remove(request.user)

    return redirect("posts:detail", pk=pk)

@login_required(login_url=reverse_lazy("users:login"))
def post_comment_view(request, pk):
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        post = get_object_or_404(models.Post, pk=pk)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post

            comment.save()

            return redirect("posts:detail", pk=pk)

        return render(request, "posts/detail.html", {"post": post, "comment_form": form})

    return redirect("posts:detail", pk=pk)


@login_required(login_url=reverse_lazy("users:login"))
def post_like_comment_view(request, pk, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(models.Comment, pk=comment_id)

        if request.user not in comment.likes.all():
            comment.likes.add(request.user)

    return redirect("posts:detail", pk=pk)


@login_required(login_url=reverse_lazy("users:login"))
def post_unlike_comment_view(request, pk, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(models.Comment, pk=comment_id)

        if request.user in comment.likes.all():
            comment.likes.remove(request.user)

    return redirect("posts:detail", pk=pk)


@login_required(login_url=reverse_lazy("users:login"))
def post_delete_comment_view(request, pk, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(models.Comment, pk=comment_id)

        if request.user == comment.author:
            comment.delete()

    return redirect("posts:detail", pk=pk)
