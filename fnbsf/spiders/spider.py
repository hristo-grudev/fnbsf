import scrapy

from scrapy.loader import ItemLoader

from ..items import FnbsfItem
from itemloaders.processors import TakeFirst


class FnbsfSpider(scrapy.Spider):
	name = 'fnbsf'
	start_urls = ['https://www.fnbsf.com/blog/']

	def parse(self, response):
		post_links = response.xpath('//button[@class="btn"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="col left"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="col-lg-8 offset-lg-1"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="post-date"]/text()').get()

		item = ItemLoader(item=FnbsfItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
