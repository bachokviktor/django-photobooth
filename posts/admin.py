from django.contrib import admin

from . import models


# Register your models here.
class PostPhotoInline(admin.StackedInline):
    model = models.PostPhoto
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [PostPhotoInline]


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment)
