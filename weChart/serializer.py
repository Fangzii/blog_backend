# coding: utf-8
from rest_framework import serializers
from .models import *


class InventorySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Inventory
        fields = ('id', 'signature')


class UserFriendSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'name', 'ownInventory')


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    friends = UserFriendSerializer(many=True)
    ownInventory = InventorySerializer(many=False)

    class Meta:
        model = User
        fields = ('id', 'name', 'friends', 'ownInventory')


class PaletteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Palette
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    image = PaletteSerializer(many=True)

    class Meta:
        model = Article
        fields = ('id','content', 'file', 'type', 'real_time', 'created_at', 'image')
