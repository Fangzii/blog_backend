# coding: utf-8
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'name', 'friends', 'ownInventory')


class InventorySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Inventory
        fields = ('id', 'signature')


class ArticleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Article
        fields = ('content', 'file', 'type', 'real_time', 'created_at',)
