# visualization

## 说明
对上次爬取的奶茶店信息可视化

参考：
[Python调用百度地图API爬取经纬度](https://zhuanlan.zhihu.com/p/55242944)
[百度地图 API 文档](http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding)
[CartoDB](https://github.com/CartoDB/carto-workshop)
[CartoDB地图可视化教程——旧金山树木分布可视化](https://www.bilibili.com/video/BV1KE411575H?from=search&seid=8027032836266682844)


### 数据处理
调用百度地图 api，得到上配地址的经纬度坐标。数据保存为 csv 格式。代码见 `prepare_data.py`

注意：使用百度地图 api 需要申请密钥，用申请到的密钥替换 `map_crawler.py` 中的 AK 值

### 可视化
TODO


