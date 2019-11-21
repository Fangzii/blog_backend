from django.shortcuts import render
import django_filters
from rest_framework import viewsets, filters,status
from rest_framework.views import APIView
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import response
from django.core import serializers
import json
from django.http import HttpResponse,JsonResponse
from .models import User, Entry, History, Pond_IP, MessageBoard, BlackList, ReplySummary, Attribute
from .serializer import UserSerializer, EntrySerializer, EntryListSerializer, EntryCreateSerializer, MessageBoardSerializer, MessageBoardCreateSerializer

class UserFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = User
        fields = ['name']

class EntryFilter(django_filters.rest_framework.FilterSet):
    search = django_filters.CharFilter(field_name='title', lookup_expr='contains', method="filter_search")

    class Meta:
        model = Entry
        fields = ['title']

    def filter_search(self, queryset, name, value):
        return queryset.filter(title__contains=value) | queryset.filter(body__contains=value)

# Create your views here
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = UserFilter

    def create(self, request, *args, **kwargs):
        if request.data:
            getData = User.objects.all()
            for obj in getData:
                if obj.name == request.data['name']:
                    return Response({"message": '名字已登记'}, status=status.HTTP_401_UNAUTHORIZED)
            data = dict(
                author=request.data['author']['id'],
                status=request.data['status'],
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
    queryset = Entry.objects.all().order_by('-id')
    serializer_class = EntrySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = EntryFilter

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
                author=request.data['author']['id'],
                status=request.data['status'],
                title=request.data['title'],
                body=request.data['body'],
                synopsis=request.data['synopsis']
            )
        self.serializer_class = EntryCreateSerializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.increase_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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

    @detail_route(methods=['get'], url_name='message')
    def message(self, request, pk=None):
        self.serializer_class = MessageBoardSerializer
        serializer = self.get_serializer(MessageBoard.objects.filter(entry_id=pk).order_by('-id'), many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'], url_name='set_message')
    def set_message(self, request, pk=None):
        # 重名处理
        try:
            a = User.objects.get(name=request.data['operator']['name'])
        except User.DoesNotExist:
            a = User(
                name=request.data['operator']['name'],
                mail=request.data['operator']['mail']
            )
            a.save()

        MessageBoard(
            operator=a,
            body=request.data['body'],
            entry=Entry.objects.get(id=pk)
        ).save()
        return Response({'success': 'true'})

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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        print(request.data)

        id = request.parser_context['kwargs']['pk']
        print(MessageBoardCreateSerializer)

        try:
            obj = User.objects.get(name=request.data['reply']['operator']['name'])
        except Exception as e:
            print(e)
            obj = {}
        if obj:
            if obj.mail == request.data['reply']['operator']['mail']:
                reply = ReplySummary(
                    operator=obj,
                    body=request.data['reply']['body']
                )
                reply.save()
                message = MessageBoard.objects.get(id=id)
                message.reply.add(reply)

            else:
                return Response({"message": "用户名重复"}, status=status.HTTP_402_PAYMENT_REQUIRED)
        else:
            a = User(
                name=request.data['reply']['operator']['name'],
                mail=request.data['reply']['operator']['mail']
            )
            a.save()
            reply = ReplySummary(
                operator=a,
                body=request.data['reply']['body']
            )
            reply.save()
            message = MessageBoard.objects.get(id=id)
            message.reply.add(reply)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({"message": "success"})

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

# 获取属性统计
@api_view(['GET'])
def view(request):
    list = []
    for e in Attribute.objects.all():
        a = Entry.objects.filter(attribute=e)
        list.append({
            'num': len(a),
            'title': e.title,
            'color': e.color
        })

    return Response({"rankings": list})


import xlwt
from django.http import HttpResponse

@api_view(['POST'])
def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="history.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('历史记录','来访时间')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['ip']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = History.objects.all().values_list('ip')
    print(rows)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response