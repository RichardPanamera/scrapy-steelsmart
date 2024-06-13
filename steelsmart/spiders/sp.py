import scrapy

class SpSpider(scrapy.Spider):
    name = "sp"
    allowed_domains = ["steelsmart.shop"]
    start_urls = ["https://steelsmart.shop/shop/telefoniya-i-aksessuary/smartfony/"]
    next_page = 0

    def parse(self, response):
        for product in response.css('div.prod-card'):
            yield {
                'name': product.css('a.prod-name::text').get(),
                'link': response.urljoin(product.css('a.prod-name::attr(href)').get()),
                'price': product.css('div.price-info span.price.semibold::text').get(),
                'cashback': product.css('div.price-cashback span::text').get(),
            }

        # Переход на следующую страницу, если она есть
        self.next_page += 1
        next_page_url = f'https://steelsmart.shop/shop/telefoniya-i-aksessuary/smartfony/?p={self.next_page}'

        # Проверка, существует ли следующая страница
        if response.css('div.prod-card'):  # Если на странице есть товары
            yield response.follow(next_page_url, self.parse)
