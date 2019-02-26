from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import User, Inventory, Article, Palette, File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    readonly_fields = ('show_file',)

    def show_file(self, obj):
        if obj.id:
            return mark_safe('<video controls="controls" width="800" height="600" name="Video Name" src="%s"></video>' % obj.file.url)

@admin.register(Palette)
class PaletteAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'ownInventory']


class PaletteAdmin(admin.TabularInline):
    model = Palette
    extra = 0




@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    pass
    # inlines = [ArticleAdmin ,]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('show_file', 'show_image')
    inlines = [PaletteAdmin, ]

    def show_file(self, obj):
        if obj.id:
            if obj.file:
                return mark_safe(
                    '<video preload="yes" loop autoplay="autoplay" controls="true" name="Video Name" src="%s"></video>' % obj.file.file.url)
            else:
                return '- 暂无视频'

    def show_image(self, obj):
        if obj.id:
            if len(obj.image.all()):
                return mark_safe(''.join(['<a href="%s" target="view_window"><img src="%s" width="300px"></img></a>' % (x.images.url, x.images.url) for x in obj.image.all()]))
            return '- 暂无图片'
