import csv
import os.path
from terminaltables import AsciiTable
import pandas as pd
import my_log


class Product:
    def __init__(self, product_id, barcode, price, brand, product_name, inventory_number, exp_date=None):
        self.product_id = product_id
        self.barcode = barcode
        self.price = price
        self.brand = brand
        self.product_name = product_name
        self.inventory_number = inventory_number
        self.exp_date = exp_date

    def create_product(self):
        try:
            file_exists = os.path.isfile('product_list.csv')
            with open('product_list.csv', 'a', newline='') as write_product_list:
                fieldnames = ['product_id', 'barcode', 'price', 'brand', 'product_name', 'inventory_number']
                csv_writer = csv.DictWriter(write_product_list, fieldnames=fieldnames)
                if not file_exists:
                    csv_writer.writeheader()
                csv_writer.writerow({'product_id': self.product_id, 'barcode': self.barcode, 'price': self.price,
                                     'brand': self.brand, 'product_name': self.product_name,
                                     'inventory_number': self.inventory_number})
        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')
            my_log.logger.error('File product_list.csv Not Found')

    @staticmethod
    def sale(username, my_choice_id, buy_basket):
        with open('product_list.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if my_choice_id == int(row['product_id']):
                    while True:
                        try:
                            count_product = int(input('Enter num for buy this product:'))
                            break
                        except ValueError:
                            print('You did not enter a number!')
                    try:
                        assert count_product <= int(row['inventory_number'])
                        new_inventory_number = int(row['inventory_number']) - count_product
                        Product.update_inventory(my_choice_id, new_inventory_number)  # if zero save in log
                        total_price = int(row['price']) * count_product
                        basket_element = ({'product_name': row['product_name'], 'price': row['price'] + ' $',
                                           'count_product': count_product, 'total_price': total_price})
                        buy_basket.append(basket_element)
                    except AssertionError:
                        print(f'inventory has {int(row["inventory_number"])} product')
                        if int(row["inventory_number"]) == 0:
                            my_log.logger.warning(f'{username} requested purchase from zero inventory.')

    @staticmethod
    def update_inventory(my_choice_id, new_inventory_number):
        try:
            df = pd.read_csv("product_list.csv")
            df.loc[my_choice_id - 1, 'inventory_number'] = new_inventory_number
            df.to_csv("product_list.csv", index=False)
            if new_inventory_number == 0:
                my_log.logger.warning(f'Inventory is empty for product_id:{my_choice_id}')
        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')
            my_log.logger.error('File product_list.csv Not Found')

    @staticmethod
    def delete_product(my_choice_id):
        try:
            df = pd.read_csv("product_list.csv")
            df = df.drop(df.index[my_choice_id - 1])
            df.to_csv("product_list.csv", index=False)
            my_log.logger.info(f'Admin delete product_id:{my_choice_id}')
        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')
            my_log.logger.error('File product_list.csv Not Found')

    @classmethod
    def show_product(cls, username):
        total_row = []
        if username == 'admin':
            table_column_headers = ['product_id', 'barcode', 'price', 'brand', 'product_name', 'inventory_number']
        else:
            table_column_headers = ['product_id', 'product_name', 'brand', 'price']
        total_row.append(table_column_headers)
        try:
            with open('product_list.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if username == 'admin':
                        rows = [row['product_id'], row['barcode'], row['price'] + ' $', row['brand'],
                                row['product_name'], row['inventory_number']]
                    else:
                        rows = [row['product_id'], row['product_name'], row['brand'], row['price'] + ' $']
                    total_row.append(rows)
        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')
            my_log.logger.error('File product_list.csv Not Found')
        else:
            data = total_row
            table = AsciiTable(data)
        return table

