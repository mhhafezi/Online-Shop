import csv
import pandas as pd
from admin import Admin
from customer import Customer
from product import Product
import my_log
from user import User


def print_menu_register_login():
    print("===============================================")
    print("""What do you want to do?\t
    1: Register\t
    2: Login\t
    3: Quit\t""")


def file_path_username_list():
    file_path = "user.csv"
    df_user_info = pd.read_csv(file_path)
    username_list = list(df_user_info['username'])
    return username_list


def len_id_product():
    """for return count of product"""
    try:
        file = open("product_list.csv")
    except FileNotFoundError:
        print('Error: File product_list.csv Not Found')
        my_log.logger.error('File product_list.csv Not Found')
    else:
        reader = csv.reader(file)
        lines = len(list(reader))
        all_id = lines - 1
    return all_id


def print_menu_admin():
    print("========================================")
    print("""What do you want to do?\t
    1: Add a product\t
    2: Show product list\t
    3: Update inventory (Recharge store inventory)\t
    4: View invoices\t
    5: Delete product\t
    6: Logout\t
    7: Go back to the main menu\t""")


def main_admin(username):
    print_menu_admin()
    choice = 0
    while choice != "7":
        choice = input("Please enter your choice:")
        if choice == "1":
            print(f'Enter information for product:')
            while True:
                try:
                    barcode = int(input('Barcode:'))
                    break
                except ValueError:
                    print('You did not enter a number!')
            while True:
                try:
                    price = int(input('Price:'))
                    break
                except ValueError:
                    print('You did not enter a number!')
            while True:
                try:
                    inventory_number = int(input('Inventory_number:'))
                    break
                except ValueError:
                    print('You did not enter a number!')
            brand = input('Brand:')
            product_name = input('Product_name:')
            Admin.add_product(barcode, price, brand, product_name, inventory_number)
            print_menu_admin()
        elif choice == "2":
            table = Product.show_product(username)
            print(table.table)
            print_menu_admin()
        elif choice == "3":
            Product.show_product(username)
            all_id = len_id_product()
            while True:
                try:
                    product_id = int(input('Enter product_id for update:'))
                    assert 0 < product_id <= all_id
                    break
                except ValueError:
                    print('You did not enter a number!')
                except AssertionError:
                    print(f'You can select id from 1-{all_id} product_id!')
            while True:
                try:
                    new_inventory_number = int(input('Enter inventory_number for add:'))
                    break
                except ValueError:
                    print('You did not enter a number!')
            Admin.add_update_inventory(product_id, new_inventory_number)
            Product.show_product(username)
            print_menu_admin()
        elif choice == "4":
            table = Admin.view_invoices(username)
            print(table.table)
            print_menu_admin()
        elif choice == "5":
            table = Product.show_product(username)
            print(table.table)
            print('Enter "product_id" for delete from product list:')
            all_id = len_id_product()
            while True:
                try:
                    my_choice_id = int(input('my_choice_id:'))
                    assert my_choice_id <= all_id
                    break
                except ValueError:
                    print('You did not enter a number!')
                except AssertionError:
                    print(f'You can select id from 1-{all_id} product_id!')
            Product.delete_product(my_choice_id)
            print_menu_admin()
        elif choice == "6":  # for user's logout
            print("\n******  Goodbye Admin ******")
            User.logout(username, 'Active', 'False')
            print_menu_register_login()
        elif choice == "7":
            print_menu_register_login()
        else:
            print("Invalid choice. Please try again.")


def print_menu_customer():
    print("===================================================")
    print("""What do you want to do?\t
    1: Buy a product\t
    2: Show all product (product_name, brand, price)\t
    3: Show my invoices\t
    4: Logout\t""")


def main_customer(username):
    print_menu_customer()
    choice = 0
    while choice != "4":
        choice = input("Please enter your choice:")
        if choice == "1":
            print(Customer.buy_product(username))
            print_menu_customer()
        elif choice == "2":
            table = Product.show_product(username)
            print(table.table)
            print_menu_customer()
        elif choice == "3":
            table = Admin.view_invoices(username)
            print(table.table)
            print_menu_customer()
        elif choice == "4":  # for user's logout
            print(f"\n******  Goodbye {username.capitalize()} ******")
            User.logout(username, 'Active', 'False')
            print_menu_register_login()
        else:
            print("Invalid choice. Please try again.")


def check_inventory():
    try:
        with open('product_list.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if int(row['inventory_number']) == 0:
                    print(
                        f'Warning inventory is zero: product_id:{row["product_id"]} product_name:{row["product_name"]}')
    except FileNotFoundError:
        print('Error: File product_list.csv Not Found')


def check_activate_account():
    try:
        with open('user_information.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row['status'] == 'Blocked':
                    print(f'{row["username"]} is "Blocked"')
    except FileNotFoundError:
        print('Error: File user_information.csv Not Found')
