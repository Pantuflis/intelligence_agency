import scrapy

# Links = ('//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href').getall()
# Title = ('//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/text()').get()
# Body = ('//div[@class="field-item even"]/p[not(@class)]/text()').get()


class SpiderCIA(scrapy.Spider):
    name = 'cia'
    start_urls = ['https://www.cia.gov/readingroom/historical-collections']
    custom_settings = {
        'FEEDS': {
            'cia.json': {
                'format': 'json',
                'encoding': 'utf-8',
            }
        },
    }

    def parse(self, response):
        links_declassified = response.xpath(
            '//a[starts-with(@href, "collection") and(parent::h3|parent::h2)]/@href').getall()
        for link in links_declassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath(
            '//h1 [@class = "documentFirstHeading"]/text()').get()
        paragraph = response.xpath(
            '//div[@class="field-item even"]/p[not(@class)]/text()').get()

        yield {
            'url': link,
            'title': title,
            'paragraph': paragraph,
        }
