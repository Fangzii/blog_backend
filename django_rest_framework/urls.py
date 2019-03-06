"""django_rest_framework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconft
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from blog.urls import router as blog_router
from blog import views

from django.conf.urls.static import static
from django_rest_framework import settings
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin/', admin.site.urls),
    #blog url
    url(r'^api/v1/', include(blog_router.urls)),
    url(r'^api/v1/test/',views.view),
    url(r'^export/xls', views.export_users_xls,),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
