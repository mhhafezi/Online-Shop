from user import User
from product import Product
import csv
from terminaltables import AsciiTable
import pandas as pd
import my_log
import os.path


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    @staticmethod
    def add_product(barcode, price, brand, product_name, inventory_number):
        try:
            with open('product_list.csv', 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 1
                for _ in csv_reader:
                    if line_count == 1:
                        product_id = 1
                        line_count += 1
                    else:
                        product_id = line_count
                        line_count += 1
        except FileNotFoundError:
            print('Error: File product_list.csv Not Found')
            my_log.logger.error('File product_list.csv Not Found')
        else:
            product_instance = Product(product_id + 1, barcode, price, brand, product_name, inventory_number)
            product_instance.create_product()
            my_log.logger.info(f'Admin add product {product_name}')
            return product_instance

    @classmethod
    def add_update_inventory(cls, product_id, new_inventory_number):
        df = pd.read_csv("product_list.csv")  # reading the csv file
        df.loc[product_id - 1, 'inventory_number'] += new_inventory_number  # updating the column 'inventory_number'
        df.to_csv("product_list.csv", index=False)  # writing into the file

    @staticmethod
    def save_to_invoice_file(username, time, sum_invoice, buy_basket):
        try:
            file_exists = os.path.isfile('invoice.csv')
            with open('invoice.csv', 'a', newline='') as write_invoice:
                fieldnames = ['customer_name', 'timestamp', 'price_invoice', 'buy_basket']
                csv_writer = csv.DictWriter(write_invoice, fieldnames=fieldnames)
                if not file_exists:
                    csv_writer.writeheader()  # file doesn't exist yet, write a header
                csv_writer.writerow(
                    {'customer_name': username, 'timestamp': time, 'price_invoice': sum_invoice,
                     'buy_basket': buy_basket})
                my_log.logger.info(f'send new invoice to customer_name: {username}')
        except FileNotFoundError:
            print('Error: File invoice.csv Not Found')

    @classmethod
    def view_invoices(cls, username):
        total_row = []
        table_column_headers = ['customer_name', 'timestamp', 'sum_invoice', 'buy_basket']
        total_row.append(table_column_headers)
        try:
            with open('invoice.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if username == 'admin':
                        rows = [row['customer_name'], row['timestamp'], row['price_invoice'] + ' $', row['buy_basket']]
                        total_row.append(rows)
                    else:
                        if row['customer_name'] == username:
                            rows = [row['customer_name'], row['timestamp'], row['price_invoice'] + ' $',
                                    row['buy_basket']]
                            total_row.append(rows)
        except FileNotFoundError:
            print('Error: File invoice.csv Not Found')
            my_log.logger.error('File invoice.csv Not Found')
        else:
            data = total_row
            table = AsciiTable(data)
        return table

    @staticmethod
    def search_by_phone(customer_phone, all_invoice_list):
        filtered_invoice_list = []
        if customer_phone:
            for invoice_ in all_invoice_list:
                if customer_phone in invoice_['costumer_name']:
                    filtered_invoice_list.append(invoice_)
            return filtered_invoice_list
        else:
            return all_invoice_list

    @staticmethod
    def search_by_date(date, all_invoice_list):
        filtered_invoice_list = []
        if date:
            for invoice_ in all_invoice_list:
                if invoice_['date'] == date:
                    filtered_invoice_list.append(invoice_)
            return filtered_invoice_list
        else:
            return all_invoice_list

    @staticmethod
    def search_by_until_date(date, all_invoice_list):
        filtered_invoice_list = []
        if date:
            for invoice_ in all_invoice_list:
                if invoice_['date'] <= date:
                    filtered_invoice_list.append(invoice_)
            return filtered_invoice_list
        else:
            return all_invoice_list
