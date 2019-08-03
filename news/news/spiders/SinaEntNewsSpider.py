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
from news.items import SinaEntNewsItem, SinaEntNewsDetailItem

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


# class SinaEntNewsSpider(RedisCrawlSpider):
class SinaEntNewsSpider(CrawlSpider):

    name = "sina_ent_news_spider"
    allowed_domains = ["sina.cn", "sina.com.cn"]
    redis_key = "sina_ent_news_spider"
    start_urls = [
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111202728545230928201_1564370486372&cre=tianyi&mod=nt_home_ent_star&merge=3&statics=1&length=15&up=0&down=0&tm=1564370493&action=0&top_id=EAbgn%2CEB55K%2CEAv3v%2C772a5c5fba87367ea2e98d0f183d3686%2CEAZw3%2CEAase%2CEAcqp%2CEAcLo%2CEAdiN%2CEAe1P%2CEB5Il%2CEB5Il%2CEAz7w%2CEAzYO%2CEB9Ng%2CEBAaL%2CEAyw3%2CEAmqB%2CEAmqB%2CEB64b%2CEAuQm%2CEAmVb&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcent%22%2C%22page_url%22%3A%22https%3A%2F%2Fent.sina.com.cn%2F%22%2C%22timestamp%22%3A1564370486377%7D&cids=34765&pdps=&smartFlow=ent_web_index_v2017_tianyistar_top&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=1000&cTime=1563679428&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112040156224285935505_1564147146345&cre=tianyi&mod=nt_home_ent_yy&merge=3&statics=1&length=15&up=0&down=0&tm=1564147497&action=0&top_id=E8qrM%2CE8qrM%2CE97sB%2CE8mUY%2CE8zHt%2CE92L9%2CE94Tx%2CE8PlT%2CE8PlT%2CE8FXH%2CE8Uy6%2CE8d87&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcent%22%2C%22page_url%22%3A%22https%3A%2F%2Fent.sina.com.cn%2F%22%2C%22timestamp%22%3A1564147146463%7D&cids=34845%2C34846%2C34848%2C34844&pdps=&smartFlow=ent_web_index_v2017_tianyimusic_top&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=1000&cTime=1563456314&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112040156224285935505_1564147146345&cre=tianyi&mod=+nt_home_ent_pic&merge=3&statics=1&up=0&down=0&tm=1564147677&action=0&top_id=E8qrM%2CE8qrM%2CE97sB%2CE8mUY%2CE8zHt%2CE92L9%2CE94Tx%2CE8PlT%2CE8PlT%2CE8FXH%2CE8Uy6%2CE8d87&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcent%22%2C%22page_url%22%3A%22https%3A%2F%2Fent.sina.com.cn%2F%22%2C%22timestamp%22%3A1564147146463%7D&cTime=1563456535&cids=7198&pdps=&smartFlow=ent_web_index_v2017_tianyiphoto_top&type=std_slide&editLevel=0%2C1%2C2%2C3&pageSize=1000&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112040156224285935505_1564147146345&cre=tianyi&mod=+nt_home_ent_movie&merge=3&statics=1&up=0&down=0&tm=1564147735&action=0&top_id=E8qrM%2CE8qrM%2CE97sB%2CE8mUY%2CE8zHt%2CE92L9%2CE94Tx%2CE8PlT%2CE8PlT%2CE8FXH%2CE8Uy6%2CE8d87&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcent%22%2C%22page_url%22%3A%22https%3A%2F%2Fent.sina.com.cn%2F%22%2C%22timestamp%22%3A1564147146463%7D&cTime=1563456566&cids=34766&pdps=&smartFlow=ent_web_index_v2017_tianyifilm_top&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=1000&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112040156224285935505_1564147146345&cre=tianyi&mod=nt_home_ent_tv&merge=3&statics=1&up=0&down=0&tm=1564147765&action=0&top_id=E8qrM%2CE8qrM%2CE97sB%2CE8mUY%2CE8zHt%2CE92L9%2CE94Tx%2CE8PlT%2CE8PlT%2CE8FXH%2CE8Uy6%2CE8d87&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcent%22%2C%22page_url%22%3A%22https%3A%2F%2Fent.sina.com.cn%2F%22%2C%22timestamp%22%3A1564147146463%7D&cTime=1563456592&cids=34816%2C34817%2C34818%2C34819&pdps=&smartFlow=ent_web_index_v2017_tianyitv_top&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=1000&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112040156224285935505_1564147146345&cre=tianyi&mod=nt_home_ent_zy&merge=3&statics=1&up=0&down=0&tm=1564147791&action=0&top_id=E8qrM%2CE8qrM%2CE97sB%2CE8mUY%2CE8zHt%2CE92L9%2CE94Tx%2CE8PlT%2CE8PlT%2CE8FXH%2CE8Uy6%2CE8d87&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcent%22%2C%22page_url%22%3A%22https%3A%2F%2Fent.sina.com.cn%2F%22%2C%22timestamp%22%3A1564147146463%7D&cTime=1563456614&cids=51889%2C51891&pdps=&smartFlow=ent_web_index_v2017_tianyizongyi_top&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=1000&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112040156224285935505_1564147146345&cre=tianyi&mod=nt_home_ent_video&merge=3&statics=1&up=0&down=0&tm=1564147887&action=0&top_id=E8qrM%2CE8qrM%2CE97sB%2CE8mUY%2CE8zHt%2CE92L9%2CE94Tx%2CE8PlT%2CE8PlT%2CE8FXH%2CE8Uy6%2CE8d87&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcent%22%2C%22page_url%22%3A%22https%3A%2F%2Fent.sina.com.cn%2F%22%2C%22timestamp%22%3A1564147146463%7D&cTime=1563456698&cids=35430&pdps=&smartFlow=ent_web_index_v2017_tianyivideo_top&type=common_video&editLevel=0%2C1%2C2%2C3&pageSize=1000&_=',
        'https://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery1112040156224285935505_1564147146345&cre=tianyi&mod=nt_home_ent_kpop&merge=3&statics=1&up=0&down=0&tm=1564147899&action=0&top_id=E8qrM%2CE8qrM%2CE97sB%2CE8mUY%2CE8zHt%2CE92L9%2CE94Tx%2CE8PlT%2CE8PlT%2CE8FXH%2CE8Uy6%2CE8d87&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcent%22%2C%22page_url%22%3A%22https%3A%2F%2Fent.sina.com.cn%2F%22%2C%22timestamp%22%3A1564147146463%7D&cTime=1563456720&cids=34805&pdps=&smartFlow=ent_web_index_v2017_tianyikorea_top&type=std_news%2Cstd_slide%2Cstd_video&editLevel=0%2C1%2C2%2C3&pageSize=1000&_='
    ]

    def parse(self, response):
        response_body = str(response.body)
        if not response_body.strip().startswith('jQuery'):
            url = response.url
            item = SinaEntNewsDetailItem()
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
                item = SinaEntNewsItem()
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
