# blog_frontend

Python版本: `3.7.1`

使用数据库: `PostgreSQL`


### 运行

```bash

createdb fang_blog_db

virtualenv -p python3 blog_frontend # 创建虚拟环境

pip install -r requierments.txt

# 每次有数据库更新时都要执行一遍，然后再migrate 为了方便部署这边的 makemigrations 是根据我自己的更新来定的，第一次运行的时候可能需要删除其中的数据库迁移
python manage.py makemigrations
 
python manage.py migrate

python manage.py createsuperuser # 创建超级用户

python manage.py runserver # 启动服务， 可在 http://localhost:8000 访问服务

celery -A django_rest_framework worker # 开启消费者


```
    
#### 说明

此项目是自用的博客项目,django admin 里有部分功能是根据自己所需建立的

项目用到几个django 插件:
 
- [ django-jet ](https://github.com/geex-arts/django-jet)  UI 优化.
- [ django-ckeditor ](https://github.com/django-ckeditor/django-ckeditor) 富文本.
- [ django-rest-framework ](https://github.com/encode/django-rest-framework) Web APIs for Django.

#### Demo (我的博客):
        
- [ fang's blog ](http://fangz-rc.work)
- [ blog 后台 ](http://fangz-rc.work/admin) 游客账号 `guest_test` 密码 `guest123`



