# -*- coding: utf-8 -*-
# @Time        : 2020/3/24 18:08
# @Author      : ssxy00
# @File        : map_crawler.py
# @Description : 调用百度地图 api，获取地点的经纬度坐标

import json
import requests

AK = "填写百度地图api密钥"

class BaiduMapCrawler:
    def __init__(self, output_type="json"):
        self.output_type = output_type # json or xml
        self.ak = AK
        # TODO request

    def get_coordinate(self, address, city="北京市"):
        url = "http://api.map.baidu.com/geocoding/v3"
        params = {"address": address,
                  "city": city,
                  "ak": self.ak,
                  "output": self.output_type}
        res = requests.get(url, params)
        coord = json.loads(res.text)['result']['location']
        return {"longitude": coord['lng'],
                "latitude": coord['lat']}


if __name__ == "__main__":
    crawler = BaiduMapCrawler()
    print(crawler.get_coordinate(address="北京大学"))