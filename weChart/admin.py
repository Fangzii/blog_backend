from django.contrib import admin

# Register your models here.
from .models import User, Inventory, Article, Palette, File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass


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
    inlines = [PaletteAdmin, ]
