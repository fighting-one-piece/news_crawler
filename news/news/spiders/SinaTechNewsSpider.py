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
from news.items import SinaTechNewsItem, SinaTechNewsDetailItem

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class SinaTechNewsSpider(CrawlSpider):

    name = "sina_tech_news_spider"
    allowed_domains = ["sina.cn", "sina.com.cn"]
    redis_key = "sina_tech_news_spider"
    start_urls = [
        'https://cre.mix.sina.com.cn/api/v3/get?callback=jQuery111204692091906118385_1564492180265&cre=tianyi&mod=pctech&merge=3&statics=1&length=15&up=0&down=0&tm=1564492201&action=0&top_id=%2CECPKG%2CECWCr%2C%2CECRmC%2CECSSI%2CECSi1%2CECTvJ%2CECTzW%2CECFv1%2CECKLL%2C%2CECNwJ%2CEC9Wo%2CEAzEm%2C%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pctech%22%2C%22page_url%22%3A%22https%3A%2F%2Ftech.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492180565%7D&cateid=1z&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111204692091906118385_1564492180265&cre=tianyi&mod=nt_home_tech_news&merge=3&statics=1&length=15&up=0&down=0&tm=1564492182&action=0&top_id=%2CECPKG%2CECWCr%2C%2CECRmC%2CECSSI%2CECSi1%2CECTvJ%2CECTzW%2CECFv1%2CECKLL%2C%2CECNwJ%2CEC9Wo%2CEAzEm%2C%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pctech%22%2C%22page_url%22%3A%22https%3A%2F%2Ftech.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492180565%7D&cids=40810%2C40811%2C40812&pdps=&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=20&cTime=1564233000&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111204692091906118385_1564492180265&cre=tianyi&mod=nt_home_tech_chuangshiji&merge=3&statics=1&length=15&up=0&down=0&tm=1564492221&action=0&top_id=%2CECPKG%2CECWCr%2C%2CECRmC%2CECSSI%2CECSi1%2CECTvJ%2CECTzW%2CECFv1%2CECKLL%2C%2CECNwJ%2CEC9Wo%2CEAzEm%2C%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pctech%22%2C%22page_url%22%3A%22https%3A%2F%2Ftech.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492180565%7D&cids=40823&pdps=&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=20&cTime=1561900255&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111204692091906118385_1564492180265&cre=tianyi&mod=nt_home_tech_mobil&merge=3&statics=1&length=15&up=0&down=0&tm=1564492255&action=0&top_id=%2CECPKG%2CECWCr%2C%2CECRmC%2CECSSI%2CECSi1%2CECTvJ%2CECTzW%2CECFv1%2CECKLL%2C%2CECNwJ%2CEC9Wo%2CEAzEm%2C%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pctech%22%2C%22page_url%22%3A%22https%3A%2F%2Ftech.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492180565%7D&cids=40813&pdps=&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=20&cTime=1563628277&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111204692091906118385_1564492180265&cre=tianyi&mod=nt_home_tech_digi&merge=3&statics=1&length=15&up=0&down=0&tm=1564492277&action=0&top_id=%2CECPKG%2CECWCr%2C%2CECRmC%2CECSSI%2CECSi1%2CECTvJ%2CECTzW%2CECFv1%2CECKLL%2C%2CECNwJ%2CEC9Wo%2CEAzEm%2C%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pctech%22%2C%22page_url%22%3A%22https%3A%2F%2Ftech.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492180565%7D&cids=40814%2C40820&pdps=&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=20&cTime=1561900290&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111204692091906118385_1564492180265&cre=tianyi&mod=nt_home_tech_discovery&merge=3&statics=1&length=15&up=0&down=0&tm=1564492291&action=0&top_id=%2CECPKG%2CECWCr%2C%2CECRmC%2CECSSI%2CECSi1%2CECTvJ%2CECTzW%2CECFv1%2CECKLL%2C%2CECNwJ%2CEC9Wo%2CEAzEm%2C%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pctech%22%2C%22page_url%22%3A%22https%3A%2F%2Ftech.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492180565%7D&cids=40821&pdps=&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=20&cTime=1562764318&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111204692091906118385_1564492180265&cre=tianyi&mod=nt_home_tech_apple&merge=3&statics=1&length=15&up=0&down=0&tm=1564492318&action=0&top_id=%2CECPKG%2CECWCr%2C%2CECRmC%2CECSSI%2CECSi1%2CECTvJ%2CECTzW%2CECFv1%2CECKLL%2C%2CECNwJ%2CEC9Wo%2CEAzEm%2C%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pctech%22%2C%22page_url%22%3A%22https%3A%2F%2Ftech.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492180565%7D&cids=40827&pdps=&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=20&cTime=1561900339&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111204692091906118385_1564492180265&cre=tianyi&mod=nt_home_tech_chuangye&merge=3&statics=1&length=15&up=0&down=0&tm=1564492340&action=0&top_id=%2CECPKG%2CECWCr%2C%2CECRmC%2CECSSI%2CECSi1%2CECTvJ%2CECTzW%2CECFv1%2CECKLL%2C%2CECNwJ%2CEC9Wo%2CEAzEm%2C%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pctech%22%2C%22page_url%22%3A%22https%3A%2F%2Ftech.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492180565%7D&cids=101658&pdps=&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=20&cTime=1561900359&_='
    ]

    def parse(self, response):
        response_body = str(response.body)
        if not response_body.strip().startswith('jQuery'):
            url = response.url
            item = SinaTechNewsDetailItem()
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
                item = SinaTechNewsItem()
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
