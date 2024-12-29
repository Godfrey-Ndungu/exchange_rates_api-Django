import scrapy


class AfricaSpider(scrapy.Spider):
    name = "Bank Of Africa"
    start_urls = ["https://boakenya.com/treasury/daily-exchange-rates/"]

    scraped_data = []

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }

    def parse(self, response):
        rows = response.xpath("//table//tbody/tr")
        
        for row in rows:
            currency = row.xpath("td[1]//text()").get().strip()
            tt_buy = row.xpath("td[2]//text()").get().replace(' ', '')
            tt_sell = row.xpath("td[3]//text()").get().replace(' ', '')
            
            if currency and tt_buy and tt_sell:
                data = {
                    "currency": currency,
                    "buy": tt_buy.strip(),
                    "sell": tt_sell.strip(),
                }
                AfricaSpider.scraped_data.append(data)
        print(AfricaSpider.scraped_data)
    def closed(self, reason):
        return AfricaSpider.scraped_data

