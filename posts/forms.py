from django import forms

from . import models


class PostForm(forms.ModelForm):
    post_photos = forms.ImageField()

    class Meta:
        model = models.Post
        fields = ["post_photos", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["post_photos"].widget.attrs.update({"multiple": "true"})
