#coding:utf-8
import scrapy
from scrapy.http import Request
from ..items import TbSpiderItem


class TbSpiderChrome(scrapy.Spider):
	name = "tb_spider_chrome"
	allowed_domains = ["taobao.com"]
	start_urls = ["http://taobao.com"]

	def parse(self, response):
		key = "沙发"
		for i in range(0,6):
			url = 'https://s.taobao.com/search?q='+str(key)+'&s='+str(i*44)
			yield Request(url=url, callback=self.parse_page)

	def parse_page(self, response):

		detail_link = response.xpath('//div[@class="item J_MouserOnverReq  "]')
		# 获取链接
		for pro in detail_link:
			url = pro.xpath('//div[@class="row row-2 title"]/a/@href').extract()[0]
			yield Request(url=url, callback=self.parse_detail)

	def parse_detail(self, response):
		item = TbSpiderItem()
		item["product_price"] = response.xpath('//dl[@id="J_PromoPrice"]//span[@class="tm-price"]/text()').extract()[0]
		
		item["product_name"] = response.xpath('//div[@class="tb-detail-hd"]/h1/text()').extract()[0].strip()

		item["product_feature"] = response.xpath('//div[@class="tb-detail-hd"]/p/text()').extract()[0].strip()

		item["product_count"] = response.xpath('//div[@class="tm-indcon"]/span[@class="tm-count"]/text()').extract()[0]

		item["comment_count"] = response.xpath('//div[@class="tm-indcon"]/span[@class="tm-count"]/text()').extract()[1]

		item["product_province"] = response.xpath('//ul[@id="J_AttrUL"]/li[1]/text()').extract()[0]

		item["product_city"] = response.xpath('//ul[@id="J_AttrUL"]/li[2]/text()').extract()[0]

		yield item
