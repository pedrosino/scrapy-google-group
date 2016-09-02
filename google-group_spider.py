import scrapy

from scrapy.utils.url import escape_ajax

class StackOverflowSpider(scrapy.Spider):
    name = 'google-group'
    start_urls = ["https://groups.google.com/forum/#!forum/django-cs"]

    def parse(self, response):
        for href in response.css('a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
        yield {
            'date': response.xpath('//td[@class="lastPostDate"]//text()').extract_first(),
            'link': response.url,
            'title': response.xpath('//h2//text()').extract()
        }