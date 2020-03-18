# dianping_crawl

## 说明
爬取大众点评上北京市的奶茶店信息

主要参考以下内容和代码：

+ [大众点评前650家咖啡店的数据分析（一）爬虫篇](https://blog.csdn.net/weixin_41013322/article/details/104702813)
[Github](https://github.com/Amberjay18/dianping_coffee_analysis)


+ [爬虫实战分享--豆瓣电影top250爬取与分析](https://zhuanlan.zhihu.com/p/62601606)

+ [Beautiful Soup 4.4.0 文档](https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/)

## 环境
Python 3.7

```
bs4
requests==2.23.0
lxml==4.5.0
fonttools==4.4.3
jsonlines==1.2.0
```

## 运行
运行前请添加 Cookie 信息，指定输出路径，以及检查大众点评当天使用的字体文件
```
python dianping_crawler.py
```

