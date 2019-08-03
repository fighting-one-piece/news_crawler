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
from news.items import SinaBlogNewsItem, SinaBlogNewsDetailItem

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class SinaBlogNewsSpider(CrawlSpider):

    name = "sina_blog_news_spider"
    allowed_domains = ["sina.cn", "sina.com.cn"]
    redis_key = "sina_blog_news_spider"
    start_urls = [
        'http://feed.mix.sina.com.cn/api/roll/get?callback=jQuery17208982132140508252_1564492716696&pageid=143&num=30&lid=3088&versionNumber=1.2.8&encode=utf-8&ctime=&_=',
        'http://feed.mix.sina.com.cn/api/roll/get?callback=jQuery17208982132140508252_1564492716698&pageid=143&num=30&lid=3089&versionNumber=1.2.8&encode=utf-8&ctime=&_=',
        'http://feed.mix.sina.com.cn/api/roll/get?callback=jQuery17208982132140508252_1564492716700&pageid=143&num=30&lid=3090&versionNumber=1.2.8&encode=utf-8&ctime=&_=',
        'http://feed.mix.sina.com.cn/api/roll/get?callback=jQuery17208982132140508252_1564492716702&pageid=143&num=30&lid=3091&versionNumber=1.2.8&encode=utf-8&ctime=&_=',
        'http://feed.mix.sina.com.cn/api/roll/get?callback=jQuery17208982132140508252_1564492716704&pageid=143&num=30&lid=3092&versionNumber=1.2.8&encode=utf-8&ctime=&_=',
        'http://feed.mix.sina.com.cn/api/roll/get?callback=jQuery17208982132140508252_1564492716706&pageid=143&num=30&lid=3093&versionNumber=1.2.8&encode=utf-8&ctime=&_=',
        'http://feed.mix.sina.com.cn/api/roll/get?callback=jQuery17208982132140508252_1564492716708&pageid=143&num=30&lid=3108&versionNumber=1.2.8&encode=utf-8&ctime=&_='
    ]

    def parse(self, response):
        response_body = str(response.body).replace('try{', '').replace(';}catch(e){};', '')
        print response_body
        if not response_body.strip().startswith('jQuery'):
            url = response.url
            item = SinaBlogNewsDetailItem()
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
            result, number = re.subn(r'jQuery\d+_\d+[(]', '', response_body)
            json_result = json.loads(result[0:len(result) - 1])
            for data in json_result['data']:
                item = SinaBlogNewsItem()
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
