import scrapy


class EquitySpider(scrapy.Spider):
    name = "equity_bank"
    start_urls = ["https://equitygroupholdings.com/ke/"]

    scraped_data = []

    def parse(self, response):
        # Select the ticker list items
        ticker_items = response.xpath("//*[@id='stocks-ticker']/li")
        print(ticker_items)
        
        # Initialize a list to hold scraped data
        self.scraped_data = []

        for item in ticker_items:
            # Extract currency pair text and remove '/KES'
            currency_pair = item.xpath("text()").get().strip().replace('/KES', '')
            buying_selling = item.xpath(".//span[@class='stat']/text()").get().strip()  # Extract buying/selling text
            
            if "Buying:" in buying_selling and "Selling:" in buying_selling:
                # Extract details from the formatted text
                parts = buying_selling.split(":")
                for part in parts:
                    if 'Buying' in part:
                        # Extract the buying number
                        buying_values = float(part.split(' ')[1].strip(','))
                    elif 'Selling' in part:
                        # Extract the selling number
                        selling_values = float(part.split(' ')[1].strip()) # Extract buying and selling prices
                
                # Extract buying and selling prices
                # buying = buying_selling_values[0].split(" ")[-1].strip()  # Extract buying price
                # selling = buying_selling_values[1].split(" ")[-1].strip()  # Extract selling price
                print(f'Parts: {parts}')
                print(f'Buying Values: {buying_values}')
                print(f'Selling Values: {selling_values}')
                # print(f'Buying Price: {buying}')
                # print(f'Selling Price: {selling}')

                
                print("----------------------------------------------------------------------")
                print("----------------------------------------------------------------------")
                print("----------------------------------------------------------------------")
                print("----------------------------------------------------------------------")          # Append to scraped data
                # self.scraped_data.append({
                #     "currency": currency_pair.strip(),  # Remove any extra spaces
                #     "buying": buying,
                #     "selling": selling,
                # })



        print(self.scraped_data)
       

    def closed(self, reason):
        """Called when the spider is closed."""
        return self.scraped_data
