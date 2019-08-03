# -*- coding:utf-8 -*-

import re
import sys
import json
import time
import scrapy
import datetime
from bs4 import BeautifulSoup
from scrapy.spiders.crawl import CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider
from news.items import SinaFashionNewsItem, SinaFashionNewsDetailItem

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class SinaFashionNewsSpider(CrawlSpider):

    name = "sina_fashion_news_spider"
    allowed_domains = ["sina.cn", "sina.com.cn"]
    redis_key = "sina_fashion_news_spider"
    start_urls = [
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112049793312661845035_1564492540720&cids=260&type=std_news%2Cstd_video%2Cstd_slide&pdps=&editLevel=0%2C1%2C2%2C3&pageSize=20&up=0&down=0&top_id=hytcerm7131571%2Chytcerm6248814%2Chytcitm4849064%2Chytcitm5366335%2Chytcerm6452298%2Chytcerm7008058%2Chytcerm7053274&mod=nt_home_fashion_latest&cTime=1561900501&action=0&tm=1564492654&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112049793312661845035_1564492540720&cids=267&type=std_news&pdps=&editLevel=0%2C1%2C2%2C3&pageSize=20&up=0&down=0&top_id=hytcerm7131571%2Chytcerm6248814%2Chytcitm4849064%2Chytcitm5366335%2Chytcerm6452298%2Chytcerm7008058%2Chytcerm7053274&mod=nt_home_fashion_style&cTime=1561900501&action=0&tm=1564492541&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112049793312661845035_1564492540720&cids=266&type=std_news&pdps=&editLevel=0%2C1%2C2%2C3&pageSize=20&up=0&down=0&top_id=hytcerm7131571%2Chytcerm6248814%2Chytcitm4849064%2Chytcitm5366335%2Chytcerm6452298%2Chytcerm7008058%2Chytcerm7053274&mod=nt_home_fashion_beauty&cTime=1561900501&action=0&tm=1564492567&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112049793312661845035_1564492540720&cids=264&type=std_news&pdps=&editLevel=0%2C1%2C2%2C3&pageSize=20&up=0&down=0&top_id=hytcerm7131571%2Chytcerm6248814%2Chytcitm4849064%2Chytcitm5366335%2Chytcerm6452298%2Chytcerm7008058%2Chytcerm7053274&mod=nt_home_fashion_life&cTime=1561900501&action=0&tm=1564492579&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112049793312661845035_1564492540720&cids=301%2C166151%2C193215&type=std_news&pdps=&editLevel=0%2C1%2C2%2C3&pageSize=20&up=0&down=0&top_id=hytcerm7131571%2Chytcerm6248814%2Chytcitm4849064%2Chytcitm5366335%2Chytcerm6452298%2Chytcerm7008058%2Chytcerm7053274&mod=nt_home_fashion_man&cTime=1561900501&action=0&tm=1564492596&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112049793312661845035_1564492540720&cids=271%2C272%2C294&type=std_news&pdps=&editLevel=0%2C1%2C2%2C3&pageSize=20&up=0&down=0&top_id=hytcerm7131571%2Chytcerm6248814%2Chytcitm4849064%2Chytcitm5366335%2Chytcerm6452298%2Chytcerm7008058%2Chytcerm7053274&mod=nt_home_fashion_chat&cTime=1561900501&action=0&tm=1564492610&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112049793312661845035_1564492540720&cids=260&type=std_video&pdps=&editLevel=0%2C1%2C2%2C3&pageSize=20&up=0&down=0&top_id=hytcerm7131571%2Chytcerm6248814%2Chytcitm4849064%2Chytcitm5366335%2Chytcerm6452298%2Chytcerm7008058%2Chytcerm7053274&mod=nt_home_fashion_video&cTime=1561900501&action=0&tm=1564492621&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112049793312661845035_1564492540720&cids=260&type=std_slide&pdps=&editLevel=0%2C1%2C2%2C3&pageSize=20&up=0&down=0&top_id=hytcerm7131571%2Chytcerm6248814%2Chytcitm4849064%2Chytcitm5366335%2Chytcerm6452298%2Chytcerm7008058%2Chytcerm7053274&mod=nt_home_fashion_photo&cTime=1561900501&action=0&tm=1564492641&_='
    ]

    def parse(self, response):
        response_body = str(response.body)
        if not response_body.strip().startswith('jQuery'):
            url = response.url
            item = SinaFashionNewsDetailItem()
            item['_id'] = url[url.rindex('/') + 1:url.rindex('.')]
            item['url'] = url
            b_soup = BeautifulSoup(response_body, 'lxml')
            title_tags = b_soup.select('body > div.main-content.w1240 > h1')
            if len(title_tags) == 0:
                title_tags = b_soup.select('body > div.F_wrap > div.F_con.clearfix > div.Vd_titBox.clearfix > h2')
            if len(title_tags) == 0:
                title_tags = b_soup.select('head > title')
            item['title'] = title_tags[0].text if len(title_tags) > 0 else None
            content_tags = b_soup.select('#artibody > p')
            if len(content_tags) == 0:
                content_tags = b_soup.select('#pl_video_info > div.vd_vedioinfo > div.vedioinfo_inner > em > p')
            if len(content_tags) == 0:
                content_tags = b_soup.select('div.swpt-table > div > div > div')
            content = ''
            for content_tag in content_tags:
                content = content + content_tag.text + '\n'
            item['content'] = content
            create_time_tags = b_soup.select('#top_bar > div > div.date-source > span.date')
            if len(create_time_tags) == 0:
                create_time_tags = b_soup.select('#pl_video_info > div.vd_vedioinfo > div.vedioinfo_inner > p.from > span > em')
            item['create_time'] = create_time_tags[0].text if len(create_time_tags) > 0 else None
            yield item
        else:
            results = re.findall(re.compile(r'[(](.*?)[)]', re.S), response_body)
            json_result = json.loads(results[0])
            for data in json_result['data']:
                item = SinaFashionNewsItem()
                item['_id'] = data['docid']
                item['doc_id'] = data['docid']
                item['f_doc_id'] = data['f_docid']
                item['author'] = data['author']
                item['tags'] = data['tags']
                item['title'] = data['title']
                item['l_title'] = data['ltitle']
                item['m_title'] = data['mtitle']
                item['s_title'] = data['stitle']
                url = data['url']
                request = scrapy.Request(url=url, method='GET')
                yield request
                item['url'] = url
                item['pc_url'] = data['pcurl']
                item['org_url'] = data['orgUrl']
                item['c_time'] = data['ctime']
                item['fp_time'] = data['fpTime']
                item['summary'] = data['summary']
                item['intro'] = data['intro']
                item['media'] = data['media']
                item['author_id'] = data['authorId']
                item['type'] = data['type']
                item['thumb'] = data['thumb']
                item['thumbs'] = data['thumbs']
                item['m_thumbs'] = data['mthumbs'] if 'mthumbs' in data else None
                item['img_count'] = data['img_count']
                item['all_model_ids'] = data['allModelIDs']
                item['labels_show'] = data['labels_show']
                item['edit_level'] = data['editLevel']
                item['level'] = data['level']
                item['uuid'] = data['uuid']
                item['info'] = data['info']
                item['new_comment_id'] = data['new_commentid']
                item['comment_id'] = data['commentid']
                item['comment_count_show'] = data['comment_count_show']
                item['comment_count'] = data['comment_count']
                item['reason'] = data['reason']
                item['user_icon'] = data['user_icon']
                item['uid'] = data['uid']
                yield item

    def start_requests(self):
        now_object = datetime.datetime.now()
        now_millisecond = long(time.mktime(now_object.timetuple()) * 1000 + now_object.microsecond / 1000)
        for start_url in self.start_urls:
            request = scrapy.Request(url=start_url + str(now_millisecond), method='GET')
            yield request
