# -*- coding: utf-8 -*-
# @Time        : 2020/3/24 17:47
# @Author      : ssxy00
# @File        : prepare_data.py
# @Description : 处理上周爬取到的数据，保存为 csv 做可视化

import csv
import json
import jsonlines
from tqdm import tqdm
from visualization.map_crawler import BaiduMapCrawler


def load_data(data_path):
    """读取爬虫爬取到的大众点评奶茶店数据"""
    dianping_data = []
    with open(data_path) as fin:
        for shop_data in jsonlines.Reader(fin):
            dianping_data.append(shop_data)
    return dianping_data

def get_coordinates(data):
    """调用百度地图 api 获取商铺的坐标"""
    map_crawler = BaiduMapCrawler()
    for shop_data in tqdm(data):
        coord = map_crawler.get_coordinate(address=shop_data['address'])
        shop_data.update(coord)
    return data

def save_csv(data, save_data_path):
    """保存为 csv"""
    with open(save_data_path, 'w') as fout:
        writer = csv.writer(fout)
        keys = list(data[0].keys())
        writer.writerow(keys)
        for data_item in data:
            writer.writerow([data_item[key] for key in keys])


def process_and_save_data():
    crawl_data_path = "../dianping_crawl/dianping_data.jsonl"
    save_data_path = "./dianping.csv"
    dianping_data = load_data(crawl_data_path)
    dianping_data = get_coordinates(dianping_data)
    save_csv(dianping_data, save_data_path)

def filter_data():
    # 过滤掉坐标不在北京市范围内的数据
    csv_path = "./dianping.csv"
    csv_save_path = "./dianping_filter.csv"
    with open(csv_path, "r") as fin:
        reader = csv.reader(fin)
        csv_data = []
        for item in reader:
            csv_data.append(item)
    longitude_idx = csv_data[0].index("longitude")
    latitude_idx = csv_data[0].index("latitude")
    with open(csv_save_path, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(csv_data[0])
        for item in csv_data[1:]:
            if 115.7 <= float(item[longitude_idx]) <= 117.4 and 39.4 <= float(item[latitude_idx]) <= 41.6:
                writer.writerow(item)

def convert_university_data():
    json_data_path = "大学-8084.json"
    csv_data_path = "university.csv"
    beijing_data = []

    with open(json_data_path) as fin:
        university_data = json.load(fin)
        print(len(university_data))

    for data_item in university_data:
        if data_item['city'] == "北京市":
            beijing_data.append({"name": data_item['name'],
                                 "longitude": data_item['location']['lng'],
                                 "latitude": data_item['location']['lat']})

    print(f"total: {len(beijing_data)} universities in Beijing")
    save_csv(beijing_data, csv_data_path)

if __name__ == "__main__":
    process_and_save_data()
    filter_data()
    convert_university_data()