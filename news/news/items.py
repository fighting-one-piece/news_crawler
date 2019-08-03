# -*- coding: utf-8 -*-

import scrapy


class SinaBaseNewsItem(scrapy.Item):
    _id = scrapy.Field()
    doc_id = scrapy.Field()
    f_doc_id = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    title = scrapy.Field()
    l_title = scrapy.Field()
    m_title = scrapy.Field()
    s_title = scrapy.Field()
    url = scrapy.Field()
    pc_url = scrapy.Field()
    org_url = scrapy.Field()
    c_time = scrapy.Field()
    fp_time = scrapy.Field()
    summary = scrapy.Field()
    intro = scrapy.Field()
    media = scrapy.Field()
    author_id = scrapy.Field()
    type = scrapy.Field()
    thumb = scrapy.Field()
    thumbs = scrapy.Field()
    m_thumbs = scrapy.Field()
    img_count = scrapy.Field()
    all_model_ids = scrapy.Field()
    labels_show = scrapy.Field()
    edit_level = scrapy.Field()
    level = scrapy.Field()
    uuid = scrapy.Field()
    info = scrapy.Field()
    new_comment_id = scrapy.Field()
    comment_id = scrapy.Field()
    comment_count_show = scrapy.Field()
    comment_count = scrapy.Field()
    reason = scrapy.Field()
    user_icon = scrapy.Field()
    uid = scrapy.Field()
    pass


class SinaBlogNewsItem(SinaBaseNewsItem):
    pass


class SinaEduNewsItem(SinaBaseNewsItem):
    pass


class SinaEntNewsItem(SinaBaseNewsItem):
    pass


class SinaFashionNewsItem(SinaBaseNewsItem):
    pass


class SinaSportsNewsItem(SinaBaseNewsItem):
    pass


class SinaTechNewsItem(SinaBaseNewsItem):
    pass


class SinaBaseNewsDetailItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    create_time = scrapy.Field()
    pass


class SinaBlogNewsDetailItem(SinaBaseNewsDetailItem):
    pass


class SinaEduNewsDetailItem(SinaBaseNewsDetailItem):
    pass


class SinaEntNewsDetailItem(SinaBaseNewsDetailItem):
    pass


class SinaFashionNewsDetailItem(SinaBaseNewsDetailItem):
    pass


class SinaSportsNewsDetailItem(SinaBaseNewsDetailItem):
    pass


class SinaTechNewsDetailItem(SinaBaseNewsDetailItem):
    pass


class NeteaseBaseNewsItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    doc_url = scrapy.Field()
    comment_url = scrapy.Field()
    t_ie_num = scrapy.Field()
    t_last_id = scrapy.Field()
    t_link = scrapy.Field()
    label = scrapy.Field()
    keywords = scrapy.Field()
    time = scrapy.Field()
    news_type = scrapy.Field()
    img_url = scrapy.Field()
    add1 = scrapy.Field()
    add2 = scrapy.Field()
    add3 = scrapy.Field()
    pass


class NeteaseArtNewsItem(NeteaseBaseNewsItem):
    pass


class NeteaseEntNewsItem(NeteaseBaseNewsItem):
    pass


class NeteaseHouseNewsItem(NeteaseBaseNewsItem):
    pass


class NeteaseMoneyNewsItem(NeteaseBaseNewsItem):
    pass


class NeteaseSportsNewsItem(NeteaseBaseNewsItem):
    pass


class NeteaseBaseNewsDetailItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    create_time = scrapy.Field()
    pass


class NeteaseArtNewsDetailItem(NeteaseBaseNewsDetailItem):
    pass


class NeteaseEntNewsDetailItem(NeteaseBaseNewsDetailItem):
    pass


class NeteaseHouseNewsDetailItem(NeteaseBaseNewsDetailItem):
    pass


class NeteaseMoneyNewsDetailItem(NeteaseBaseNewsDetailItem):
    pass


class NeteaseSportsNewsDetailItem(NeteaseBaseNewsDetailItem):
    pass
