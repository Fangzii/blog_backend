from django.contrib import admin
from .models import User, Entry, History, Pond_IP, BlackList, MessageBoard, ReplySummary, UserInformatization


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'mail'
    ]


@admin.register(UserInformatization)
class UserInformatization(admin.ModelAdmin):
    pass


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    pass


@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = [
        'ip',
        'created_at',
        'updated_at',
        'intercept_number'
    ]

@admin.register(Pond_IP)
class PondAdmin(admin.ModelAdmin):
    list_display = [
        'ip',
        'created_at',
        'updated_at',
        'visit_number'
    ]

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = [
        'visit_time',
        'ip',
        'location',
        'entrance',
        'country',
        'area',
        'region',
        'city',
        'isp',
        'access_tools',
        'action'
    ]

    readonly_fields = 'visit_time', 'ip', 'location', 'entrance', 'country', 'area', 'region', 'city', 'isp', 'access_tools', 'JSON', 'action'

    actions = ['sync_location']

    def sync_location(self,request, queryset):
        for obj in queryset:
            obj.find_location()

        self.message_user(request=request, message='同步成功 %s 条数据' % len(queryset))
    sync_location.short_description = '同步位置'


@admin.register(MessageBoard)
class PondAdmin(admin.ModelAdmin):
    list_display = [
        "operator",
        "body",
        "get_reply",
        "created_at",
        "updated_at"
    ]




@admin.register(ReplySummary)
class PondAdmin(admin.ModelAdmin):
    list_display = [
        "operator",
        "body",
        "created_at",
        "updated_at"
    ]



admin.site.site_header = "fang's blog 管理"
admin.site.index_title = '管理主页'