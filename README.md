#SpiderFrame

##介绍
这是爬虫框架集合，是在scrapy 基础上添加的，主要做的工作：
* scrapy爬取基本配置：redis通道，MySQL通道，本地存储，日志配置
* 实现并配置scrapy图片抓取
* 封装了google_images_download 现在图片
* 封装了 you-get 视频抓取框架便于scrapy 调用
* 封装了 pytube 框架（这是抓取youtube的专用框架）

## 注意事项
* 使用google要翻墙
* 在spiderframe/spiderframe下启动爬虫，否则会报没有日志文件夹

## 下一步需要做的工作
* 提高视频下载速度
* 封装的视频框架调用函数，没有很好的解决参数问题
* 封装的pytube，可以进行字幕和音频流抓取，需要封装
* 图片视频抓取后一个粗筛选器
* 修改没有在spiderframe/spiderframe启动时报没有日志文件夹bug

##说明
spiders文件夹中有四个文件，image_699pic.py video.bilibili.py video.youtube.py vietnam_news_vn_link.py
这是开发时候测试文件，不想写 test文件夹了，就这样吧，等我认为完美了再整理测试文件
