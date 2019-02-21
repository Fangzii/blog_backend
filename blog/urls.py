# coding: utf-8
from rest_framework import routers
from .views import UserViewSet, EntryViewSet, view, MessageBoardViewSet
from weChart import views
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'entries', EntryViewSet)
router.register(r'messageboard', MessageBoardViewSet)
router.registry(r'user',views.UserViewSets,base_name="user")
router.registry(r'inventory', views.InventoryViewSet)
router.registry(r'article', views.ArticleViewSet)

# router.registry(r'test1',test)
