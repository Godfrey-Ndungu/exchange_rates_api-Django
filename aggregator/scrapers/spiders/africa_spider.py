import scrapy


class AfricaSpider(scrapy.Spider):
    name = "bank_of_africa"
    start_urls = ["https://boakenya.com/treasury/daily-exchange-rates/"]

    scraped_data = []

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

