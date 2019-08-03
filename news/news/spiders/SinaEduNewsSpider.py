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
from news.items import SinaEduNewsItem, SinaEduNewsDetailItem

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class SinaEduNewsSpider(CrawlSpider):

    name = "sina_edu_news_spider"
    allowed_domains = ["sina.cn", "sina.com.cn"]
    redis_key = "sina_edu_news_spider"
    start_urls = [
        'http://cre.mix.sina.com.cn/api/v3/get?callback=jQuery1112005743528697848377_1564492879436&cre=tianyi&mod=pcedu&merge=3&statics=1&length=60&up=0&down=0&tm=1564493069&action=0&top_id=%2CEBz6t%2CEC8Kw%2C%2CE68Fa%2CEC78i%2CEAzzx%2CEBION%2CDyVWZ%2C%2C%2C%2CEBzzg%2CECYMV%2CEC7lv%2CEC9mp%2CEC8fB%2CEC7xZ%2C%2CEBEJA%2C%2C%2CEB77d%2CEB8DT%2CEB7o8%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcedu%22%2C%22page_url%22%3A%22http%3A%2F%2Fedu.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492879463%7D&cateid=I&_=',
        'http://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112005743528697848377_1564492879436&cre=tianyi&mod=nt_home_edu_zxx&merge=3&statics=1&length=60&up=0&down=0&tm=1564492961&action=0&top_id=%2CEBz6t%2CEC8Kw%2C%2CE68Fa%2CEC78i%2CEAzzx%2CEBION%2CDyVWZ%2C%2C%2C%2CEBzzg%2CECYMV%2CEC7lv%2CEC9mp%2CEC8fB%2CEC7xZ%2C%2CEBEJA%2C%2C%2CEB77d%2CEB8DT%2CEB7o8%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcedu%22%2C%22page_url%22%3A%22http%3A%2F%2Fedu.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492879463%7D&cids=80446%2C80453%2C80441&pdps=&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=20&_=',
        'http://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112005743528697848377_1564492879436&cre=tianyi&mod=nt_home_edu_gk&merge=3&statics=1&length=60&up=0&down=0&tm=1564492881&action=0&top_id=%2CEBz6t%2CEC8Kw%2C%2CE68Fa%2CEC78i%2CEAzzx%2CEBION%2CDyVWZ%2C%2C%2C%2CEBzzg%2CECYMV%2CEC7lv%2CEC9mp%2CEC8fB%2CEC7xZ%2C%2CEBEJA%2C%2C%2CEB77d%2CEB8DT%2CEB7o8%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcedu%22%2C%22page_url%22%3A%22http%3A%2F%2Fedu.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492879463%7D&cids=80440&pdps=&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=20&_=',
        'http://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112005743528697848377_1564492879436&cre=tianyi&mod=nt_home_edu_gjxx&merge=3&statics=1&length=60&up=0&down=0&tm=1564492983&action=0&top_id=%2CEBz6t%2CEC8Kw%2C%2CE68Fa%2CEC78i%2CEAzzx%2CEBION%2CDyVWZ%2C%2C%2C%2CEBzzg%2CECYMV%2CEC7lv%2CEC9mp%2CEC8fB%2CEC7xZ%2C%2CEBEJA%2C%2C%2CEB77d%2CEB8DT%2CEB7o8%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcedu%22%2C%22page_url%22%3A%22http%3A%2F%2Fedu.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492879463%7D&cids=80448&pdps=&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=20&_=',
        'http://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112005743528697848377_1564492879436&cre=tianyi&mod=nt_home_edu_hy&merge=3&statics=1&length=60&up=0&down=0&tm=1564493007&action=0&top_id=%2CEBz6t%2CEC8Kw%2C%2CE68Fa%2CEC78i%2CEAzzx%2CEBION%2CDyVWZ%2C%2C%2C%2CEBzzg%2CECYMV%2CEC7lv%2CEC9mp%2CEC8fB%2CEC7xZ%2C%2CEBEJA%2C%2C%2CEB77d%2CEB8DT%2CEB7o8%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcedu%22%2C%22page_url%22%3A%22http%3A%2F%2Fedu.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492879463%7D&cids=188640&pdps=&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=20&cTime=1561901020&_=',
        'http://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112005743528697848377_1564492879436&cre=tianyi&mod=nt_home_edu_ks&merge=3&statics=1&length=60&up=0&down=0&tm=1564493021&action=0&top_id=%2CEBz6t%2CEC8Kw%2C%2CE68Fa%2CEC78i%2CEAzzx%2CEBION%2CDyVWZ%2C%2C%2C%2CEBzzg%2CECYMV%2CEC7lv%2CEC9mp%2CEC8fB%2CEC7xZ%2C%2CEBEJA%2C%2C%2CEB77d%2CEB8DT%2CEB7o8%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcedu%22%2C%22page_url%22%3A%22http%3A%2F%2Fedu.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492879463%7D&cids=80442%2C80443%2C80449&pdps=&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=20&cTime=1561901020&_=',
        'http://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112005743528697848377_1564492879436&cre=tianyi&mod=nt_home_edu_cg&merge=3&statics=1&length=60&up=0&down=0&tm=1564493049&action=0&top_id=%2CEBz6t%2CEC8Kw%2C%2CE68Fa%2CEC78i%2CEAzzx%2CEBION%2CDyVWZ%2C%2C%2C%2CEBzzg%2CECYMV%2CEC7lv%2CEC9mp%2CEC8fB%2CEC7xZ%2C%2CEBEJA%2C%2C%2CEB77d%2CEB8DT%2CEB7o8%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcedu%22%2C%22page_url%22%3A%22http%3A%2F%2Fedu.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492879463%7D&cids=80450&pdps=&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=20&cTime=1561901020&_=',
        'http://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112005743528697848377_1564492879436&cre=tianyi&mod=nt_home_edu_kj&merge=3&statics=1&length=60&up=0&down=0&tm=1564493055&action=0&top_id=%2CEBz6t%2CEC8Kw%2C%2CE68Fa%2CEC78i%2CEAzzx%2CEBION%2CDyVWZ%2C%2C%2C%2CEBzzg%2CECYMV%2CEC7lv%2CEC9mp%2CEC8fB%2CEC7xZ%2C%2CEBEJA%2C%2C%2CEB77d%2CEB8DT%2CEB7o8%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcedu%22%2C%22page_url%22%3A%22http%3A%2F%2Fedu.sina.com.cn%2F%22%2C%22timestamp%22%3A1564492879463%7D&cids=80539&pdps=&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=20&cTime=1561901020&_='
    ]

    def parse(self, response):
        response_body = str(response.body)
        if not response_body.strip().startswith('jQuery'):
            url = response.url
            item = SinaEduNewsDetailItem()
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
                item = SinaEduNewsItem()
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
