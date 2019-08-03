# -*- coding: utf-8 -*-

import pymongo
import traceback
from news.items import SinaBlogNewsItem, SinaEduNewsItem, SinaEntNewsItem, SinaFashionNewsItem, SinaSportsNewsItem, SinaTechNewsItem,\
    SinaBlogNewsDetailItem, SinaEduNewsDetailItem, SinaEntNewsDetailItem, SinaFashionNewsDetailItem, SinaSportsNewsDetailItem, SinaTechNewsDetailItem
from news.items import NeteaseBaseNewsItem, NeteaseArtNewsItem, NeteaseEntNewsItem, NeteaseHouseNewsItem, \
    NeteaseMoneyNewsItem, NeteaseSportsNewsItem, NeteaseBaseNewsDetailItem, NeteaseArtNewsDetailItem, \
    NeteaseEntNewsDetailItem, NeteaseHouseNewsDetailItem, NeteaseMoneyNewsDetailItem, NeteaseSportsNewsDetailItem


class ConsolePipeline(object):

    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(host='192.168.0.125', port=27017)
        self.db = self.client['news']

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.client.close()
        pass

    def process_item(self, item, spider):
        try:
            if isinstance(item, SinaBlogNewsItem):
                self.db['sina_blog_news'].insert(dict(item))
            elif isinstance(item, SinaEduNewsItem):
                self.db['sina_edu_news'].insert(dict(item))
            elif isinstance(item, SinaEntNewsItem):
                self.db['sina_ent_news'].insert(dict(item))
            elif isinstance(item, SinaFashionNewsItem):
                self.db['sina_fashion_news'].insert(dict(item))
            elif isinstance(item, SinaSportsNewsItem):
                self.db['sina_sports_news'].insert(dict(item))
            elif isinstance(item, SinaTechNewsItem):
                self.db['sina_tech_news'].insert(dict(item))
            elif isinstance(item, SinaBlogNewsDetailItem):
                self.db['sina_blog_news_detail'].insert(dict(item))
            elif isinstance(item, SinaEduNewsDetailItem):
                self.db['sina_edu_news_detail'].insert(dict(item))
            elif isinstance(item, SinaEntNewsDetailItem):
                self.db['sina_ent_news_detail'].insert(dict(item))
            elif isinstance(item, SinaFashionNewsDetailItem):
                self.db['sina_fashion_news_detail'].insert(dict(item))
            elif isinstance(item, SinaSportsNewsDetailItem):
                self.db['sina_sports_news_detail'].insert(dict(item))
            elif isinstance(item, SinaTechNewsDetailItem):
                self.db['sina_tech_news_detail'].insert(dict(item))
            elif isinstance(item, NeteaseArtNewsItem):
                self.db['netease_art_news'].insert(dict(item))
            elif isinstance(item, NeteaseEntNewsItem):
                self.db['netease_ent_news'].insert(dict(item))
            elif isinstance(item, NeteaseHouseNewsItem):
                self.db['netease_house_news'].insert(dict(item))
            elif isinstance(item, NeteaseMoneyNewsItem):
                self.db['netease_money_news'].insert(dict(item))
            elif isinstance(item, NeteaseSportsNewsItem):
                self.db['netease_sports_news'].insert(dict(item))
            elif isinstance(item, NeteaseBaseNewsItem):
                self.db['netease_news'].insert(dict(item))
            elif isinstance(item, NeteaseArtNewsDetailItem):
                self.db['netease_art_news_detail'].insert(dict(item))
            elif isinstance(item, NeteaseEntNewsDetailItem):
                self.db['netease_ent_news_detail'].insert(dict(item))
            elif isinstance(item, NeteaseHouseNewsDetailItem):
                self.db['netease_house_news_detail'].insert(dict(item))
            elif isinstance(item, NeteaseMoneyNewsDetailItem):
                self.db['netease_money_news_detail'].insert(dict(item))
            elif isinstance(item, NeteaseSportsNewsDetailItem):
                self.db['netease_sports_news_detail'].insert(dict(item))
            elif isinstance(item, NeteaseBaseNewsDetailItem):
                self.db['netease_news_detail'].insert(dict(item))
        except pymongo.errors.DuplicateKeyError:
            pass
        except Exception, e:
            print e.message
            print traceback.format_exc()
        return item


