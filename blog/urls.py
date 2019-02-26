# coding: utf-8
from rest_framework import routers
from .views import UserViewSet, EntryViewSet, view, MessageBoardViewSet
from weChart import views
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name="users")
router.register(r'entries', EntryViewSet)
router.register(r'messageboard', MessageBoardViewSet)

router.register(r'user',views.UserViewSets, base_name="user")
router.register(r'inventory', views.InventoryViewSet)
router.register(r'article', views.ArticleViewSet)
