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


class PostUpdateForm(forms.ModelForm):
    new_photos = forms.ImageField(required=False)

    class Meta:
        model = models.Post
        fields = ["new_photos", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["new_photos"].widget.attrs.update({"multiple": "true"})
