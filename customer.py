from admin import Admin
from product import Product
from terminaltables import AsciiTable
import datetime
import menu


class Customer(Admin):
    def __init__(self, username, password, total_price=0):
        super().__init__(username, password)
        self.total_price = total_price

    @staticmethod
    def buy_product(username):
        all_id = menu.len_id_product()
        buy_basket = []  # basket for add basket_element with count and total-price for each product is selected
        stop = False
        while not stop:
            print('Enter "product_id" and count from above table to buy a product. press "0" for stop.')
            while True:
                try:
                    my_choice_id = int(input('my_choice_id:'))
                    assert my_choice_id <= all_id
                    break
                except ValueError:
                    print('You did not enter a number!')
                except AssertionError:
                    print(f'You can select id from 1-{all_id} product_id!')
            if my_choice_id != 0:
                Product.sale(username, my_choice_id, buy_basket)
            else:
                stop = True
        sum_invoice = sum([int(product['total_price']) for product in buy_basket])
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Admin.save_to_invoice_file(username, time, sum_invoice, buy_basket)  # for save invoice to invoice.csv

        return Customer.show_buy_basket(buy_basket, sum_invoice, time)

    @staticmethod
    def show_buy_basket(buy_basket, sum_invoice, time):
        total_row = []
        table_column_headers = ['product_name', 'price', 'count_product', 'total_price']
        total_row.append(table_column_headers)
        for product in buy_basket:
            product_row = [product['product_name'], product['price'], product['count_product'], product['total_price']]
            total_row.append(product_row)
        data = total_row
        table = AsciiTable(data)
        return f"Your buy_basket is:\n {table.table}\n Your price_invoice is: {sum_invoice} $ \n Time: {time}"
