from django.contrib import admin
from .models import File, Image, Emotions_work
# Register your models here.


@admin.register(Emotions_work)
class EmotionsWorkAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'get_file_url',
        'get_image_url',
        'created_at',
        'updated_at',
    ]
    filter_horizontal = ('file', 'image')


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass