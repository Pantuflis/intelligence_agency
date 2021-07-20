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
        'CURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['test@outlook.com.ar'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Pepito',
        'FEED_EXPORT_ENCODING': 'UTF-8',
    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
            authors = kwargs['authors']

        quotes.extend(response.xpath(
            '//div[@class="quote"]/span[@class="text"]/text()').getall())
        authors.extend(response.xpath(
            '//small[@class="author"]/text()').getall())

        quotes_and_authors = list(zip(quotes, authors))
        # for i in range(len(quotes)):
        #     quotes_and_authors.append(quotes[i] + ' by ' + authors[i])

        next_page_button_link = response.xpath(
            '//ul[@class="pager"]/li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'authors': authors})
        else:
            yield {
                'quotes_and_authors': quotes_and_authors,
            }

    def parse(self, response):
        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath(
            '//div[@class="quote"]/span[@class="text"]/text()').getall()
        authors = response.xpath('//small[@class="author"]/text()').getall()
        top_tags = response.xpath(
            '//span[@class="tag-item"]/a[@class="tag"]/text()').getall()
        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            top_tags = top_tags[:top]
        yield {
            'title': title,
            'top_tags': top_tags
        }

        next_page_button_link = response.xpath(
            '//ul[@class="pager"]/li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'authors': authors})
