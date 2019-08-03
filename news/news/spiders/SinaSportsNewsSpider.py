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
from news.items import SinaSportsNewsItem, SinaSportsNewsDetailItem

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class SinaSportsNewsSpider(CrawlSpider):

    name = "sina_sports_news_spider"
    allowed_domains = ["sina.cn", "sina.com.cn"]
    redis_key = "sina_sports_news_spider"
    start_urls = [
        'http://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111303880791352957953_1564491811710&cre=tianyi&mod=nt_home_sports_nba&merge=3&statics=1&tm=1564491815&offset=0&action=0&up=0&down=0&cids=57316&pdps=&top_id=&smartFlow=&editLevel=0%2C+1%2C+2%2C+3%2C+4&pageSize=12&type=sports_news%2Csports_slide%2Csports_video%2C+common_video_sports&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcspt%22%2C%22page_url%22%3A%22http%3A%2F%2Fsports.sina.com.cn%2F%22%2C%22timestamp%22%3A1564491811830+%7D&_=',
        'http://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111303880791352957953_1564491811710&cre=tianyi&mod=nt_home_sports_global&merge=3&statics=1&tm=1564491845&offset=0&action=0&up=0&down=0&cids=57307&pdps=&top_id=&smartFlow=&editLevel=0%2C+1%2C+2%2C+3%2C+4&pageSize=12&type=sports_news%2C+sports_slide%2C+sports_video%2C+common_video_sports&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcspt%22%2C%22page_url%22%3A%22http%3A%2F%2Fsports.sina.com.cn%2F%22%2C%22timestamp%22%3A1564491811830+%7D&_=',
        'http://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111303880791352957953_1564491811710&cre=tianyi&mod=nt_home_sports_china&merge=3&statics=1&tm=1564491881&offset=0&action=0&up=0&down=0&cids=57299&pdps=&top_id=&smartFlow=&editLevel=0%2C+1%2C+2%2C+3%2C+4&pageSize=12&type=sports_news%2C+sports_slide%2C+sports_video%2C+common_video_sports&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcspt%22%2C%22page_url%22%3A%22http%3A%2F%2Fsports.sina.com.cn%2F%22%2C%22timestamp%22%3A1564491811829+%7D&_=',
        'http://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111303880791352957953_1564491811710&cre=tianyi&mod=nt_home_sports_cba&merge=3&statics=1&tm=1564491899&offset=0&action=0&up=0&down=0&cids=57317%2C57318%2C57319&pdps=&top_id=&smartFlow=&editLevel=0%2C+1%2C+2%2C+3%2C+4&pageSize=12&type=sports_news%2C+sports_slide%2C+sports_video%2C+common_video_sports&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcspt%22%2C%22page_url%22%3A%22http%3A%2F%2Fsports.sina.com.cn%2F%22%2C%22timestamp%22%3A1564491811830+%7D&_=',
        'http://cre.mix.sina.com.cn/get/cms/feed?callback=jQuery111303880791352957953_1564491811710&pcProduct=33&ctime=&merge=3&mod=pcsptw&cre=tianyi&statics=1&length=12&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcspt%22%2C%22page_url%22%3A%22http%3A%2F%2Fsports.sina.com.cn%2F%22%2C%22timestamp%22%3A1564491811830+%7D&_=',
        'http://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111303880791352957953_1564491811710&cre=tianyi&mod=nt_home_sports_pic&merge=3&statics=1&tm=1564491961&offset=0&action=0&up=0&down=0&cids=56510&pdps=&top_id=&smartFlow=&editLevel=0%2C+1%2C+2%2C+3%2C+4&pageSize=12&type=sports_slide&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcspt%22%2C%22page_url%22%3A%22http%3A%2F%2Fsports.sina.com.cn%2F%22%2C%22timestamp%22%3A1564491811830+%7D&_=',
        'http://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111303880791352957953_1564491811710&cre=tianyi&mod=nt_home_sports_video&merge=3&statics=1&tm=1564492057&offset=0&action=0&up=0&down=0&cids=56510&pdps=&top_id=&smartFlow=&editLevel=0%2C+1%2C+2%2C+3%2C+4&pageSize=12&type=sports_video%2C+common_video_sports&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcspt%22%2C%22page_url%22%3A%22http%3A%2F%2Fsports.sina.com.cn%2F%22%2C%22timestamp%22%3A1564491811830+%7D&_='
    ]

    def parse(self, response):
        response_body = str(response.body)
        if not response_body.strip().startswith('jQuery'):
            url = response.url
            item = SinaSportsNewsDetailItem()
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
                item = SinaSportsNewsItem()
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
