import django_filters
from rest_framework import viewsets
from .serializer import *
from .models import User, Inventory, Article

# Create your views here.


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class ArticleFilter(django_filters.rest_framework.FilterSet):
    search = django_filters.CharFilter(field_name='content', lookup_expr='contains')

    class Meta:
        model = Article
        fields = ['inventory_article', 'search']


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = ArticleFilter

