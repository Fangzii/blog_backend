from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.


class File(models.Model):

    file_name = models.CharField(max_length=32, verbose_name="文件名称")
    file = models.FileField(upload_to='uploadFile', blank=True)
    summarize = models.CharField(max_length=32, verbose_name="文件概述")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name


class Image(models.Model):

    image_name = models.CharField(max_length=32, verbose_name="图片名称")
    image = models.ImageField(verbose_name="图片", upload_to='uploadImages', blank=True,)
    summarize = models.CharField(max_length=32, verbose_name="图片描述")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image_name


class Emotions_work(models.Model):

    name = models.CharField(max_length=32, verbose_name="名称")
    file = models.ManyToManyField(File, verbose_name="文件")
    image = models.ManyToManyField(Image, verbose_name="图片")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    def get_file_url(self):
        return mark_safe('/'.join(['<a href="%s">%s</a>' % (x.file.url, x.file_name) for x in self.file.get_queryset()]))
    get_file_url.short_description='文件'

    def get_image_url(self):
        return mark_safe('/'.join(['<a href="%s">%s</a>' % (x.image.url, x.image_name) for x in self.image.get_queryset()]))
    get_image_url.short_description = '图像'

    def __str__(self):
        return "%s - %s" % (self.name, self.created_at)