# -*- coding:utf-8 -*-

import re
import sys
import json
import time
import scrapy
from bs4 import BeautifulSoup
from scrapy.spiders.crawl import CrawlSpider
from news.items import NeteaseBaseNewsItem, NeteaseBaseNewsDetailItem

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class NeteaseNewsSpider(CrawlSpider):

    name = "netease_news_spider"
    allowed_domains = ["163.com", "temp.163.com", "house.163.com"]
    redis_key = "netease_news_spider"
    start_urls = [
        'https://temp.163.com/special/00804KVA/cm_guonei.js?callback=data_callback',
        'https://temp.163.com/special/00804KVA/cm_guoji.js?callback=data_callback',
        'https://temp.163.com/special/00804KVA/cm_dujia.js?callback=data_callback',
        'https://temp.163.com/special/00804KVA/cm_war.js?callback=data_callback',
        'https://temp.163.com/special/00804KVA/cm_money.js?callback=data_callback',
        'https://temp.163.com/special/00804KVA/cm_tech.js?callback=data_callback',
        'https://temp.163.com/special/00804KVA/cm_sports.js?callback=data_callback',
        'https://temp.163.com/special/00804KVA/cm_ent.js?callback=data_callback',
        'https://temp.163.com/special/00804KVA/cm_lady.js?callback=data_callback',
        'https://temp.163.com/special/00804KVA/cm_auto.js?callback=data_callback',
        'https://temp.163.com/special/00804KVA/cm_houseshanghai.js?callback=data_callback',
        'https://temp.163.com/special/00804KVA/cm_hangkong.js?callback=data_callback',
        'https://temp.163.com/special/00804KVA/cm_jiankang.js?callback=data_callback',
        'https://house.163.com/special/00078GU7/beijing_xw_news_v1.js?callback=data_callback',
        'https://house.163.com/special/00078GU7/shenzhen_xw_news_v1.js?callback=data_callback',
        'https://house.163.com/special/00078GU7/guangzhou_xw_news_v1.js?callback=data_callback',
        'https://house.163.com/special/00078GU7/hangzhou_xw_news_v1.js?callback=data_callback',
        'https://house.163.com/special/00078GU7/nanjing_xw_news_v1.js?callback=data_callback',
        'https://house.163.com/special/00078GU7/wuhan_xw_news_v1.js?callback=data_callback',
        'https://house.163.com/special/00078GU7/jinan_xw_news_v1.js?callback=data_callback',
        'https://house.163.com/special/00078GU7/wulumuqi_xw_news_v1.js?callback=data_callback',
        'https://house.163.com/special/00078GU7/haikou_xw_news_v1.js?callback=data_callback',
        'https://house.163.com/special/00078GU7/xiamen_xw_news_v1.js?callback=data_callback',
        'https://house.163.com/special/00078GU7/suzhou_xw_news_v1.js?callback=data_callback',
        'https://house.163.com/special/00078GU7/guiyang_xw_news_v1.js?callback=data_callback',
        'https://house.163.com/special/00078GU7/chengdu_xw_news_v1.js?callback=data_callback',
        'https://house.163.com/special/00078GU7/nanchong_xw_news_v1.js?callback=data_callback'
    ]

    def parse(self, response):
        response_body = response.body
        try:
            response_body = response_body.decode('gbk')
        except Exception, e:
            print e.message
        if not response_body.strip().startswith('data_callback'):
            resp_url = response.url
            item = NeteaseBaseNewsDetailItem()
            item['_id'] = resp_url[resp_url.rindex('/') + 1:resp_url.rindex('.')]
            item['url'] = resp_url
            b_soup = BeautifulSoup(response_body, 'lxml')
            title_tags = b_soup.select('#epContentLeft > h1')
            if len(title_tags) == 0:
                title_tags = b_soup.select('body > div.gallery > div > div.headline > h1')
            item['title'] = title_tags[0].text if len(title_tags) > 0 else None
            content = ''
            content_tags = b_soup.select('#endText > p')
            if len(content_tags) == 0:
                content_tags = b_soup.select('div.viewport > div.overview > p')
            for content_tag in content_tags:
                content = content + str(content_tag.text).strip() + '\n'
            item['content'] = content
            create_time_tags = b_soup.select('#epContentLeft > div.post_time_source')
            if len(create_time_tags) == 0:
                create_time_tags = b_soup.select('body > div.gallery > div > div.headline > span')
            item['create_time'] = str(create_time_tags[0].text).strip()[0:19] if len(create_time_tags) > 0 else None
            yield item
        else:
            result = response_body.replace('data_callback(', '').replace('])', ']')
            json_result = json.loads(result)
            for data in json_result:
                item = NeteaseBaseNewsItem()
                doc_url = data['docurl']
                request = scrapy.Request(url=doc_url, method='GET')
                yield request
                item['_id'] = doc_url[doc_url.rindex('/') + 1:doc_url.rindex('.')]
                item['title'] = data['title']
                item['doc_url'] = doc_url
                item['comment_url'] = data['commenturl']
                item['t_ie_num'] = data['tienum']
                item['t_last_id'] = data['tlastid']
                item['t_link'] = data['tlink']
                item['label'] = data['label']
                item['keywords'] = data['keywords']
                item['time'] = data['time']
                item['news_type'] = data['newstype']
                item['img_url'] = data['imgurl']
                item['add1'] = data['add1']
                item['add2'] = data['add2']
                item['add3'] = data['add3']
                yield item

    def start_requests(self):
        for start_url in self.start_urls:
            start_url = start_url + '&' + str(int(time.time()))
            request = scrapy.Request(url=start_url, method='GET')
            yield request
