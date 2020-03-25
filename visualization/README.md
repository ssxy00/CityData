# visualization

## 说明
对上次爬取的奶茶店信息可视化

参考：

[Python调用百度地图API爬取经纬度](https://zhuanlan.zhihu.com/p/55242944)

[百度地图 API 文档](http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding)

[CartoDB](https://github.com/CartoDB/carto-workshop)

[CartoDB地图可视化教程——旧金山树木分布可视化](https://www.bilibili.com/video/BV1KE411575H?from=search&seid=8027032836266682844)

[中国所有学校地理位置Json数据库](https://github.com/pg7go/The-Location-Data-of-Schools-in-China)

### 数据处理
1. 调用百度地图 api，得到上配地址的经纬度坐标。

数据保存为 csv 格式。代码见 `prepare_data.process_and_save_data`

注意：使用百度地图 api 需要申请密钥，用申请到的密钥替换 `map_crawler.py` 中的 AK 值

2. 过滤掉不在北京坐标范围内的数据点 `prepare_data.filter_data`

3. 获取北京高校的地理坐标

这里直接用了 github 上找到的数据，[数据链接](https://github.com/pg7go/The-Location-Data-of-Schools-in-China/blob/master/%E5%A4%A7%E5%AD%A6-8084.json)

只提取北京市的高校，数据处理成 csv 格式 `prepare_data.convert_university_data`

### 可视化
使用 CartoDB 平台做可视化

结果见 `./figures`



