## 爬虫

执行crawler/crawler中crawl.py文件，一共可爬到18000多条新闻

## 搜索

- 执行main.py
- 两个简易api
    - boolean search 目前只支持连续的&&查询
        - http://localhost:5000/api/boolean?keyword={空格连接的关键词}
        - 比如: http://localhost:5000/api/boolean?keyword=senior_official
    - specific search 目前只支持根据日期和新闻源查询
        - http://localhost:5000/api/specific?date={日期}&source={媒体源}
        - 比如: http://localhost:5000/api/specific?date=2020-11-03&source=globaltimes
