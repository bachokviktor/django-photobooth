from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models, forms


# Create your views here.
def empty(request):
    return HttpResponse("<h2>Empty page</h2>")


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

            return redirect("posts:home")

        return render(request, self.template_name, {"form": form})
