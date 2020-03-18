# -*- coding: utf-8 -*-
# @Time        : 2020/3/17 23:32
# @Author      : ssxy00
# @File        : dianping_crawler.py
# @Description :

import requests
import time
import jsonlines
from typing import List, Dict
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont
from font_files.texts import TEXTS


class DianpingCrawler:
    def __init__(self, address_font_file_path: str, num_font_file_path: str):
        self.character_list = TEXTS
        self.address_font_dict = self.get_font_dict(address_font_file_path)
        self.num_font_dict = self.get_font_dict(num_font_file_path)
        self.cookie = {Your Cookie}
        self.headers = {
            "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': self.cookie,
            'Host': 'www.dianping.com',
            'Referer': "https://www.dianping.com/beijing/ch10/g34237",
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }

    def get_font_dict(self, font_file_path: str) -> Dict[str, str]:
        """载入字体文件，创建 字符编码 -> 字符 的字典"""
        font = TTFont(font_file_path)
        font_dict = {}
        # 获取所有字体的上面对应的编码
        font_names = font.getGlyphOrder()
        for idx, character in enumerate(self.character_list):
            code = font_names[idx].replace('uni', '&#x').lower() + ';'
            font_dict[code] = character
        return font_dict

    def clean_html(self, html: str) -> str:
        """处理字体反爬"""
        for code in self.num_font_dict:
            html = html.replace(code, self.num_font_dict[code])

        for code in self.address_font_dict:
            html = html.replace(code, self.address_font_dict[code])

        return html

    def get_page_shops_info(self, url: str) -> List[dict]:
        """返回当前页面上所有店铺的信息"""
        page_shops_info = []
        html = requests.get(url, headers=self.headers).text
        html = self.clean_html(html)
        soup = BeautifulSoup(html, 'lxml')
        milk_tea_info = soup.find('div', id='shop-all-list')
        shops = milk_tea_info.find_all('li', class_="")
        for shop in shops:
            # 店铺名称
            shop_name = shop.find('h4').get_text()
            # 地址
            address = shop.find('span', class_='addr').get_text()
            # 人均价格
            mean_price = shop.find('a', class_='mean-price').find('b')
            if mean_price is None:  # 处理缺失
                mean_price = -1
            else:
                mean_price = mean_price.get_text().replace(' ', '')  # "￥22"
                if mean_price.startswith('￥'):
                    mean_price = mean_price[1:]
                    mean_price = int(mean_price)

            # 评论数
            review_num = shop.find('a', class_='review-num').find('b')
            if review_num is None:  # 处理缺失
                review_num = -1
            else:
                review_num = review_num.get_text().replace(' ', '')
                review_num = int(review_num)
            # 是否支持外卖
            if shop.find('a', class_='tuan') is not None:
                takeaway = True
            else:
                takeaway = False

            page_shops_info.append({'shop_name': shop_name,
                                    'address': address,
                                    'mean_price': mean_price,
                                    "review_num": review_num,
                                    'takeaway': takeaway})
        return page_shops_info


def get_page_url_list() -> List[str]:
    """返回 北京/饮品店/茶饮果汁 分类下 50 页的 urls"""
    base_url = "https://www.dianping.com/beijing/ch10/g34237"  # 第一页
    page_url_list = [base_url]
    for i in range(2, 51):
        page_url_list.append(base_url + f"p{i}")
    return page_url_list


def main():
    save_path = "dianping_data.jsonl"
    address_font_file_path = "font_files/2e01b109.woff"
    num_font_file_path = "font_files/6360abca.woff"
    crawler = DianpingCrawler(address_font_file_path=address_font_file_path,
                              num_font_file_path=num_font_file_path)
    shops_info = []  # 存储爬取到的所有店铺的信息
    # 大众点评可以显示某个类别下 50 页的信息，获取这 50 页的 url
    page_url_list = get_page_url_list()
    # 爬取数据
    for idx, url in enumerate(page_url_list, 1):
        print(f"Now crawling page {idx} ... ")
        try:
            page_shops_info = crawler.get_page_shops_info(url)
            shops_info += page_shops_info
            print(f"This page has {len(page_shops_info)} shops")
        except:
            print(url)
        time.sleep(10)  # 据说点评的反爬做的比较好，所以这里等待时间设的大一些
    with jsonlines.open(save_path, 'a') as writer:
        for shop_info in shops_info:
            writer.write(shop_info)

if __name__ == "__main__":
    main()
