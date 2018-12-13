from django.shortcuts import render
import django_filters
from rest_framework import viewsets, filters,status
from rest_framework.views import APIView
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import response
from .models import User, Entry, History, Pond_IP, MessageBoard, BlackList
from .serializer import UserSerializer, EntrySerializer, EntryListSerializer, EntryCreateSerializer, MessageBoardSerializer, MessageBoardCreateSerializer

# Create your views here
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        if request.data:
            getData = User.objects.all()
            for obj in getData:
                if obj.name == request.data['name']:
                    return Response({"message": '名字已登记'}, status=status.HTTP_401_UNAUTHORIZED)
            data = dict(
                author = request.data['author']['id'],
                status =request.data['status'],
                title=request.data['title'],
                body=request.data['body'],
            )
        self.serializer_class = EntryCreateSerializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    def list(self, request, *args, **kwargs):
        self.watchDog(request)
        #访问权限后期再改
        # if self.watchDog(request):
        #     return Response({"message": "无访问权限"}, status=status.HTTP_403_FORBIDDEN)

        self.serializer_class = EntryListSerializer
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)


        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.data:
            data = dict(
                author = request.data['author']['id'],
                status =request.data['status'],
                title=request.data['title'],
                body=request.data['body'],
            )
        self.serializer_class = EntryCreateSerializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def watchDog(self, request):
        # 增加访问历史
        History.objects.create(
            ip=request.META.get('REMOTE_ADDR'),
            access_tools=request.META.get('HTTP_USER_AGENT'),
            JSON=request.META,
            entrance='list',
        )

        # 记录来访ip
        try:
            ip = Pond_IP.objects.get(ip=request.META.get('REMOTE_ADDR'))
        except Exception as e:
            print(e)
            ip = {}

        if Pond_IP.objects.all() and ip:
            Pond = Pond_IP.objects.get(ip=request.META.get('REMOTE_ADDR'))
            Pond.visit_number += 1
            Pond.save()
        else:
            Pond_IP.objects.create(
                ip=request.META.get('REMOTE_ADDR'),
            )

        try:
            black_ip = BlackList.objects.get(ip=request.META.get('REMOTE_ADDR'))
        except Exception as e:
            print(e)
            black_ip = {}

        if BlackList.objects.all() and black_ip:
            #  拦击记录
            black_ip.intercept_number += 1
            black_ip.save()
            return True


class MessageBoardViewSet(viewsets.ModelViewSet):
    queryset = MessageBoard.objects.all().order_by('-id')
    serializer_class = MessageBoardSerializer


    def create(self, request, *args, **kwargs):

        if self.watchDog(request):
            return Response({"message": "无访问权限"}, status=status.HTTP_403_FORBIDDEN)

        try:
            obj = User.objects.get(name=request.data['operator']['name'])
        except Exception as e:
            print(e)
            obj = {}

        if obj:
            if obj.mail == request.data['operator']['mail']:
                data = dict(
                    operator=obj.id,
                    body=request.data['body']
                )
            else:
                return Response({"message": "用户名重复"}, status=status.HTTP_402_PAYMENT_REQUIRED)
        else:
            a = User(
                name=request.data['operator']['name'],
                mail=request.data['operator']['mail']
            )
            a.save()
            data = dict(
                operator=a.id,
                body=request.data['body']
            )

            # 创建用户记录登记
            History.objects.create(
                ip=request.META.get('REMOTE_ADDR'),
                access_tools=request.META.get('HTTP_USER_AGENT'),
                JSON=request.META,
                entrance='createUser',
                action='用户: %s 邮箱: %s' % (
                request.data['operator']['name'], request.data['operator']['mail'])
            )

        self.serializer_class = MessageBoardCreateSerializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def list(self, request, *args, **kwargs):
    #     if self.watchDog(request):
    #         return Response({"message": "无访问权限"}, status=status.HTTP_403_FORBIDDEN)
    #
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #
    #     return Response(serializer.data)

    def watchDog(self, request):

        try:
            ip = BlackList.objects.get(ip=request.META.get('REMOTE_ADDR'))
        except Exception as e:
            print(e)
            ip = {}

        if BlackList.objects.all() and ip:
            # 拦截记录
            ip.intercept_number += 1
            ip.save()

            return True

        if request.data:
            History.objects.create(
                ip=request.META.get('REMOTE_ADDR'),
                access_tools=request.META.get('HTTP_USER_AGENT'),
                JSON=request.META,
                entrance='messageBoard',
                action='内容: %s 中间人: %s 邮箱: %s' % (request.data['body'],request.data['operator']['name'],request.data['operator']['mail'])
            )

@api_view(['POST'])
def view(request):
    print(request.data)
    # 暂时权限登入 后期加表
    if request.data['name'] == 'hahahaha' and request.data['password'] == 'hahahaha':
        return Response({"message": "success"})

    return Response({"message": "无访问权限"}, status=status.HTTP_403_FORBIDDEN)