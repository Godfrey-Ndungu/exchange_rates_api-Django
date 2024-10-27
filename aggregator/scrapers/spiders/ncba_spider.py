import scrapy


class NcbaSpider(scrapy.Spider):
    name = "ncba_bank"
    start_urls = ["https://ke.ncbagroup.com/forex-rates/"]

    scraped_data = []

    def parse(self, response):
        rows = response.css("table.table-bordered tbody tr")
        for row in rows:
            data = {
                "currency": row.css("td:nth-child(2)::text").get(),
                "buy": row.css("td:nth-child(3)::text").get(),
                "sell": row.css("td:nth-child(4)::text").get(),
            }
            NcbaSpider.scraped_data.append(data)

    def closed(self, reason):
        """Called when the spider is closed."""
        return self.scraped_data
