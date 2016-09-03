import scrapy

from scrapy.utils.url import escape_ajax

class StackOverflowSpider(scrapy.Spider):
  name = 'login'
  start_urls = ["https://accounts.google.com/ServiceLogin?hl=pt-BR#identifier"]

  def parse(self, response):
    """
    Insert the email. Next, go to the password page.
    """
    return scrapy.FormRequest.from_response(
      response,
      formdata={'Email': self.user_name},
      callback=self.log_password)

  def log_password(self, response):
    """
    Enter the password to complete the log in.
    """
    return scrapy.FormRequest.from_response(
      response,
      formdata={'Passwd': self.user_pass},
      callback=self.after_login)

  def after_login(self, response):
    return scrapy.Request("https://groups.google.com/forum/?_escaped_fragment_=forum/wca-delegates[1-100]", callback=self.parse_forum)

  def parse_forum(self, response):
    for href in response.css('a::attr(href)'):
      full_url = response.urljoin(href.extract())
      if "5B" in full_url:
        yield scrapy.Request(full_url, callback=self.parse_forum)
      yield scrapy.Request(full_url, callback=self.parse_thread)

  def parse_thread(self, response):
    yield {
      'date': response.xpath('//td[@class="lastPostDate"]//text()').extract_first(),
      'link': response.url,
      'title': response.xpath('//h2//text()').extract()
    }