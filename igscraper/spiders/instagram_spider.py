#!/usr/bin/env python3

import json
import re
import scrapy

from igscraper import items

class InstagramSpider(scrapy.Spider):
    name = "instagram"

    def __init__(self, tag='', *args, **kwargs):
        super(InstagramSpider, self).__init__(*args, **kwargs)
        self.tag = tag
        self.base_url = "https://www.instagram.com/explore/tags/%s/?__a=1" % tag
        self.start_urls = [self.base_url]
        self.download_delay = 1.5
        self.limit = 1     # number of pages crawl for each tag
        self.count = 0

    def parse(self, response):

        response = json.loads(response.body.decode('utf-8'))
        data = response['tag']['media']['nodes']

        for post in data:

            if "caption" in post:
                caption = post['caption']
                tags_re = re.compile(r"#(\w+)")
                tags = tags_re.findall(caption)

                post_id = post['id']
                is_video = post['is_video']
                likes = post['likes']['count']
                comments = post['comments']['count']
                date = post['date']
                media = post['thumbnail_src']

                yield items.IgscraperItem({
                    'post_id': post_id,
                    'is_video': is_video,
                    'caption': caption,
                    'tags': tags,
                    'likes': likes,
                    'comments': comments,
                    'date': date,
                    'media': media
                })

        if response['tag']['media']['page_info']['has_next_page'] and self.count < self.limit:
            self.count += 1
            end_cursor = response['tag']['media']['page_info']['end_cursor']
            yield scrapy.Request(self.base_url + "&max_id=%s" % end_cursor)