# -*- coding: utf-8 -*-
# @Time        : 2020/3/24 17:47
# @Author      : ssxy00
# @File        : prepare_data.py
# @Description : 处理上周爬取到的数据，保存为 csv 做可视化

import csv
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
        for shop_data in data:
            writer.writerow([shop_data[key] for key in keys])


def process_and_save_data():
    crawl_data_path = "../dianping_crawl/dianping_data.jsonl"
    save_data_path = "./dianping.csv"
    dianping_data = load_data(crawl_data_path)
    dianping_data = get_coordinates(dianping_data)
    save_csv(dianping_data, save_data_path)

if __name__ == "__main__":
    process_and_save_data()