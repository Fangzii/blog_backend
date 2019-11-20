# coding: utf-8
from rest_framework import serializers
from .models import User, Entry, MessageBoard, ReplySummary, UserInformatization


class UserInformatizationSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = UserInformatization
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    informatization = UserInformatizationSerializer(many=False)

    class Meta:
        model = User
        fields = ('id', 'name', 'informatization')


# 不显示用户邮箱来确保用户隐私
class UserSafeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name',)


class EntrySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = UserSafeSerializer(many=False, read_only=False)
    # author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Entry
        fields = ('id','title','body','created_at','status','author','views','synopsis')


class EntryListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = UserSafeSerializer(many=False, read_only=False)

    class Meta:
        model = Entry
        fields = ('id','title','created_at','status','author', 'views','synopsis')


class EntryCreateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Entry
        fields = ('id','title','created_at','status','author','body','synopsis')


class ReplySummarySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    operator = UserSafeSerializer(many=False, read_only=False)

    class Meta:
        model = ReplySummary
        fields = ('id', 'body', 'created_at', 'operator')

class ReplySummaryCreateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = ReplySummary
        fields = ('id', 'body', 'created_at', 'operator',)

class MessageBoardSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    operator = UserSafeSerializer(many=False, read_only=False)
    reply = ReplySummarySerializer(many=True)

    class Meta:
        model = MessageBoard
        fields = ('id', 'body', 'created_at', 'operator','reply',)

class MessageBoardCreateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = MessageBoard
        fields = ('id', 'body', 'created_at', 'operator','reply')