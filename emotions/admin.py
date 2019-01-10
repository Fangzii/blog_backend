from django.contrib import admin
from .models import File, Image, Emotions_work
# Register your models here.


@admin.register(Emotions_work)
class EmotionsWorkAdmin(admin.ModelAdmin):
    filter_horizontal = ('file', 'image')


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass