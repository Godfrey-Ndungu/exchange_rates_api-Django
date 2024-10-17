import scrapy


class NCBASpider(scrapy.Spider):
    name = "ncba_bank"
    start_urls = ["https://ke.ncbagroup.com/forex-rates/"]

    def parse(self, response):
        rows = response.css("table.table-bordered tbody tr")
        for row in rows:
            data = {
                "currency": row.css("td:nth-child(2)::text").get(),
                "buy": row.css("td:nth-child(3)::text").get(),
                "sell": row.css("td:nth-child(4)::text").get(),
            }
            print(data)
            yield data
