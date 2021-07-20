import scrapy

# Titulo = ('//h1/a/text()').get()
# Citas = ('//div[@class="quote"]/span/text()').getall()
# Top ten tags = ('//span[@class="tag-item"]/a[@class="tag"]/text()').getall()
# Next page button = ('//ul[@class="pager"]/li[@class="next"]/a/@href').get()


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']

    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
    }

    def parse(self, response):
        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath(
            '//div[@class="quote"]/span[@class="text"]/text()').getall()
        top_tags = response.xpath(
            '//span[@class="tag-item"]/a[@class="tag"]/text()').getall()
        yield {
            'title': title,
            'quotes': quotes,
            'top_ten_tags': top_tags
        }

        next_page_button_link = response.xpath(
            '//ul[@class="pager"]/li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse)
