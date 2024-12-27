import scrapy

class ImSpider(scrapy.Spider):
    name = "im_bank"
    start_urls = ["https://www.imbankgroup.com/ke/foreign-exchange/"]

    scraped_data = []
    
    def parse(self, response):
        rows = response.css("table.table-striped tbody tr")

        for row in rows:
            currency_pair = row.css("td:nth-child(2)::text").get().replace('/ KES', '').replace('KES /', '').replace(':', '').strip()
            bank_buy_tt = row.css("td:nth-child(5)::text").get(default='').strip().replace(':', '')
            bank_sell_tt = row.css("td:nth-child(6)::text").get(default='').strip().replace(':', '')
            data = {
                "currency": currency_pair,
                "buy": bank_buy_tt,
                "sell": bank_sell_tt,
            }

            ImSpider.scraped_data.append(data)
    
    def closed(self, reason):
        print(ImSpider.scraped_data)
        return ImSpider.scraped_data
