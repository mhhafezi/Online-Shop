from datetime import datetime


class Invoice:
    def __init__(self, shop, costumer_phone_number, products):
        self.market_name = shop
        self.costumer_phone = costumer_phone_number
        self.products = products
        self.total_price = self.calculate_total_price()
        self.date = str(datetime.now())

    def calculate_total_price(self):
        total_price = 0
        for item in self.products:
            total_price += int(item["price"])
        return total_price
