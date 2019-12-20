
import urllib.request
import json
# import time
from .models import History

url = 'http://ip-api.com/json/'


def checkTaobaoIP():
    for i in History.objects.all().order_by('-id'):
        if i.location == None or i.location == '查询错误...':
            print(i.location, i.ip)

            try:
                import requests
                # 淘宝IP地址库接口
                r = requests.get(url + i.ip + '?lang=zh-CN')

                # r.json()
                data = r.json()
                print(r.json())
                i.country = data['country']  # 国家
                # i.area = data['area']  # 区域
                i.region = data['regionName']  # 地区
                i.city = data['city']  # 城市
                i.isp = data['isp']  # 运营商

                i.location = u'国家: %s\n区域: %s\n省份: %s\n城市: %s\n运营商: %s\n' % (i.country, i.area, i.region, i.city, i.isp)
                print(u'国家: %s\n区域: %s\n省份: %s\n城市: %s\n运营商: %s\n' % (i.country, i.area, i.region, i.city, i.isp))
                print(i)
                i.save()

            except:
                checkTaobaoIP()
