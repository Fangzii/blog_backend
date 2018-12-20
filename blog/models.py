from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=32)
    mail = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PUBLIC = "public"
    STATUS_SET = (
            (STATUS_DRAFT,"草稿"),
            (STATUS_PUBLIC,"公开"),
    )
    title = models.CharField(max_length=128)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_SET, default=STATUS_DRAFT, max_length=8)
    author = models.ForeignKey(User, related_name='entries',on_delete=models.CASCADE)
    # view = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def increase_views(self):
        self.view += 1
        self.save(update_fields=['views'])


class History(models.Model):

    visit_time = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=128, null=True)
    location = models.CharField(max_length=128, null=True,)
    entrance = models.CharField(max_length=128, null=True,)
    country = models.CharField(max_length=128, null=True,)
    area = models.CharField(max_length=128, null=True,)
    region = models.CharField(max_length=128, null=True,)
    city = models.CharField(max_length=128, null=True,)
    isp = models.CharField(max_length=128, null=True,)
    access_tools = models.CharField(max_length=128, null=True,)
    JSON = models.TextField(null=True,)
    action = models.TextField(null=True,)

    def __str__(self):
        return self.ip

    def get_ip(self):
        pass

    def find_location(self):
        import requests
        # 淘宝IP地址库接口
        r = requests.get('http://ip.taobao.com/service/getIpInfo.php?ip=%s' % self.ip)
        if r.json()['code'] == 0:
            i = r.json()['data']

            self.country = i['country']  # 国家
            self.area = i['area']  # 区域
            self.region = i['region']  # 地区
            self.city = i['city']  # 城市
            self.isp = i['isp']  # 运营商

            self.location = u'国家: %s\n区域: %s\n省份: %s\n城市: %s\n运营商: %s\n' % (self.country, self.area, self.region, self.city, self.isp)
            self.save();
        else:
            print("ERRO! ip: %s" % self.ip)

class Pond_IP(models.Model):

    ip = models.CharField(max_length=128, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='开始时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='上次来访时间')
    visit_number = models.IntegerField(default=1, null=True, verbose_name='来访次数', editable=False)

    def __str__(self):
        return self.ip

class ReplySummary(models.Model):

    operator = models.ForeignKey(User, related_name='operatorReply',on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.operator.name, self.created_at)

class MessageBoard(models.Model):

    operator = models.ForeignKey(User, related_name='operator', on_delete=models.CASCADE)
    body = models.TextField()
    reply = models.ManyToManyField(ReplySummary, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.operator.name, self.created_at)

    def get_reply(self):
        print('-------------')
        print(self.reply.all())
        return "\n".join([p.body for p in self.reply.all()])

class BlackList(models.Model):

    ip = models.OneToOneField(Pond_IP, on_delete=models.CASCADE,  primary_key=True,)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='上次拦截时间')
    intercept_number = models.IntegerField(default=0, null=True, verbose_name='拦截次数', editable=False)

    def __str__(self):
        return self.ip.ip


class AdminInformation(models.Model):

    name = models.CharField(max_length=128, primary_key=True, blank=False)
    password = models.CharField(max_length=50)
    mail = models.EmailField()
    git = models.CharField(max_length=128, null=True)
    url = models.CharField(max_length=128, null=True)
    weChat = models.CharField(max_length=128, null=True)
    location = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.name
