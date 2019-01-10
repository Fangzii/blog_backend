from django.db import models

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

    name = models.CharField(max_length=32)
    file = models.ManyToManyField(File)
    image = models.ManyToManyField(Image)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.name, self.created_at)