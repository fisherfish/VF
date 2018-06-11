from django.contrib import admin

from .models import VideoComments


class VideoCommentsAdmin(admin.ModelAdmin):
    pass


admin.site.register(VideoComments, VideoCommentsAdmin)

# Register your models here.
