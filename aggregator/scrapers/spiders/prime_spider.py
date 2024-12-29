import scrapy


class PrimeSpider(scrapy.Spider):
    name = "Prime"
    start_urls = ["https://www.primebank.co.ke/todays-exchange-rates/"]

    scraped_data = []

    def parse(self, response):
        rows = response.xpath("//table[@class='tafe-table']//tbody//tr")
        
        for row in rows:
            currency = row.xpath("td[1]//text()").get()
            if currency:
                currency = currency.strip().split()[-1]  # Remove image and keep currency code (e.g., 'USD')

            # Extract TT Buy, TT Sell, Cash Buy, Cash Sell values
            tt_buy = row.xpath("td[2]//text()").get()
            tt_sell = row.xpath("td[3]//text()").get()
            cash_buy = row.xpath("td[4]//text()").get()
            cash_sell = row.xpath("td[5]//text()").get()
            
            # Ensure all values are extracted and clean
            if currency and tt_buy and tt_sell:
                # Clean and validate the numeric values
                try:
                    buy = Decimal(tt_buy.strip().replace(' ', ''))
                    sell = Decimal(tt_sell.strip().replace(' ', ''))
                    cash_buy = Decimal(cash_buy.strip().replace(' ', '')) if cash_buy else None
                    cash_sell = Decimal(cash_sell.strip().replace(' ', '')) if cash_sell else None
                    
                    # Prepare the data for appending
                    data = {
                        "currency": currency,
                        "buy": str(buy),
                        "sell": str(sell),
                        "cash_buy": str(cash_buy) if cash_buy else None,
                        "cash_sell": str(cash_sell) if cash_sell else None
                    }
                    scraped_data.append(data)
                except InvalidOperation as e:
                    self.logger.error(f"Failed to convert values for {currency}: {e}")
        
        print(PrimeSpider.scraped_data)
    def closed(self, reason):
        return PrimeSpider.scraped_data

