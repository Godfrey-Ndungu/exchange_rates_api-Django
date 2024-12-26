import scrapy


class EquitySpider(scrapy.Spider):
    name = "equity_bank"
    start_urls = ["https://equitygroupholdings.com/ke/"]

    scraped_data = []

    def parse(self, response):
        ticker_items = response.xpath("//*[@id='stocks-ticker']/li")
        self.scraped_data = []

        for item in ticker_items:
            currency_pair = item.xpath("text()").get().strip().replace('/KES', '').replace(':', '')
            buying_selling = item.xpath(".//span[@class='stat']/text()").get().strip()
            parts = buying_selling.replace(",", " ").replace(":", " ").split()
            data = {
                "currency": currency_pair, 
                "buy": parts[1],
                "sell": parts[3],
            }
            EquitySpider.scraped_data.append(data)

    def closed(self, reason):
        print(EquitySpider.scraped_data)
        return EquitySpider.scraped_data
