# SpiderFrame

## 介绍
    这是爬虫框架集合，是在scrapy 基础上添加的，主要做的工作：
* scrapy爬取基本配置：redis通道，MySQL通道，本地存储，日志配置
* 实现并配置scrapy图片抓取
* 封装了google_images_download 现在图片
* 封装了 you-get 视频抓取框架便于scrapy 调用
* 封装了 pytube 框架（这是抓取youtube的专用框架）

## 注意事项
* 使用google要翻墙
* 在spiderframe/spiderframe下启动爬虫，否则会报没有日志文件夹

## 命名规范
* 图片抓取爬虫image_网站名   eg: image_360
* 视频抓取 video_网站名_link存储到redis 再由video_base统一下载下来   eg: video_bilibili_link
* 其他任务 语言名_任务名_网站名_其他    eg: china_news_people_link


## 文件夹说明
* common 公共文件夹，用于存放需要的公共函数
* file  用于存放抓取到的文件，本地主要用于调试，服务器用于大规模抓取，主要是图片，视频文件服务器还有 /data/video/video 文件夹
* script 用于爬取需要的脚本文件，其他框架抓取的集成
* spider 爬虫文件
* download.py 不使用scrapy 的下载, 方便在spider中调用
* items.py item 文件
* main.py 爬虫启动主文件
* middlewares.py 中间件
* pipelines.py 管道文件
* settings.py 爬虫设置文件
* .gitignore   git忽略文件
* requirment.txt  依赖文件
* scrapy.cfg 配置文件
