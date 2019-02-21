from django.db import models
# Create your models here.


class File(models.Model):

    file_name = models.CharField(max_length=32,)
    file = models.FileField(upload_to='uploadFile', blank=True)
    imageDescription = models.CharField(max_length=128, verbose_name='文件描述', blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_file_name(self):
        return self.file.name.split('/')[1]

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = "文件"
        verbose_name_plural = verbose_name


class Article(models.Model):

    TYPE_IMAGE = 'image'
    TYPE_VIDEO = 'video'
    TYPE_SET = (
        (TYPE_IMAGE, "图像"),
        (TYPE_VIDEO, "视频"),
    )
    content = models.TextField(blank=True)
    file = models.OneToOneField(File, blank=True, on_delete=models.CASCADE, null=True)
    type = models.CharField(choices=TYPE_SET, default=TYPE_IMAGE, max_length=8)
    real_time = models.DateTimeField(verbose_name="真实创建时间", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.content, self.created_at)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name

class Inventory(models.Model):

    signature = models.CharField(max_length=32, blank=True, verbose_name='签名')
    article = models.ManyToManyField(Article, blank=True, related_name="inventory_article")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_user(self):
        try:
            name = '%s的朋友圈' % User.objects.get(ownInventory=self).name
        except Exception as e:
            print(e)
            name = '暂无归属'
        return name

    def __str__(self):
        return self.get_user()

    class Meta:
        verbose_name = "朋友圈"
        verbose_name_plural = verbose_name


class Palette(models.Model):

    parents = models.ForeignKey(Article, related_name='image', on_delete=models.CASCADE)
    images_name = models.CharField(max_length=32, null=True, blank=True)
    images = models.ImageField(verbose_name="图片", upload_to='uploadImages', blank=True, )
    imageDescription = models.CharField(max_length=128, verbose_name='图片描述', blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     #     if self.images_name:
    #     #         return self.images_name
    #     #     else:
    #     #         return self.parents_id

    class Meta:
        verbose_name = "图片"
        verbose_name_plural = verbose_name


class User(models.Model):

    name = models.CharField(max_length=32)
    friends = models.ManyToManyField('self', blank=True,)
    ownInventory = models.OneToOneField(Inventory, on_delete=models.CASCADE, blank=True, verbose_name="朋友圈")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name



