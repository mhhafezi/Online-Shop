import my_log
import sys
import hashlib
from validations import validation_time, validation_password, validation_phone_number, username_exists
from shop import Shop
from customer import Customer
from File_Handler import UsersFileHandler


def password_hashing(password):
    """
    :param password: takes the password that you want to hash
    :return: hashed password
    """
    hashed_password = hashlib.sha256(password.encode())
    return hashed_password.hexdigest()


def user_info(username):
    """
    returns information of the given user
    :param username: username of desired user
    """
    users = UsersFileHandler()
    for user in users.read_file():
        if user["username"] == username:
            return user


def add_product(shop):
    """
    inputs information of a product to add to the given shop
    :param shop: name of the shop
    """
    choice = '1'
    while choice == '1':
        product_name = input("Enter product name : ")
        brand = input("Enter brand : ")
        product_count = input("Enter Inventory : ")
        product_price = input("Enter price : ")
        barcode = input("Enter serial number or barcode : ")
        expiration_date = input("Enter expiration date with format Day-Month-Year with leading zeros(03-12-2021): ")
        Shop.add_product_to_shop(shop=shop, name_of_product=product_name, brand=brand, product_inventory=product_count,
                                 product_price=product_price, serial=barcode, expiration_date=expiration_date)
        my_log.logger.info(f"{shop} shop added {product_name} product with exp date: {expiration_date}")
        choice = input("Do you want to add more products?\n 1. Yes 2. No ")


def main_menu():
    """
    the main menu that is printed for user!
    """
    print("=" * 25)
    print("What do you want to do?")
    print('1. Sign Up')
    print('2. Sign In')
    print('3. Exit')
    print("=" * 25)
    choice = input("Enter your choice: \n")
    if choice == "1":
        register_user()
    elif choice == "2":
        sign_in()
    elif choice == "3":
        my_log.logger.info("Exited from the main menu!")
        sys.exit()
    else:
        my_log.logger.info("Wrong choice for the main menu!")
        main_menu()


def manager_menu(username):
    """
    the manager menu that is printed for user!
    """
    print("=" * 25)
    print('Manager Menu')
    print("""What do you want to do?\n
    1. Add a product'\n2. View Products\n
    3. Check unavailable products\n4. View all invoices\n
    5. Invoice search\n6. View all costumers and their invoices\n
    7. View list of all costumers\n8. Block a costumer\n
    9. Back to main menu\n10. Exit\n""")
    print("=" * 25)
    choice = input('What is your choice: \n')
    if choice == '1':
        add_product(username)
        manager_menu(username)
    elif choice == '2':
        Shop.shop_products(username)
        manager_menu(username)
    elif choice == '3':
        Shop.shop_inventory_warning(username)
        manager_menu(username)
    elif choice == '4':
        Shop.shop_invoices(username)
        manager_menu(username)
    elif choice == '5':
        customer_phone = input('Enter customer phone number for search or'
                               ' press Enter if you do not want to search by it: ')
        date = input('Enter date or press Enter if you do not want to search by it')
        interval_date = input('Enter date or press Enter')
        Shop.search_shop_invoice(username, customer_phone, date, interval_date)
        manager_menu(username)
    elif choice == '6':
        Shop.shop_customers_info(username)
        manager_menu(username)
    elif choice == '7':
        Shop.shop_customer_list(username)
        manager_menu(username)
    elif choice == '8':
        customers = Shop.shop_customer_list(username)
        if customers:
            costumer = input('Enter Username of costumer you want to block: ')
            Shop.block_customer(username, costumer)
            print(f'customer with username : {costumer} blocked successfully')
            my_log.logger.info(f"{username} blocked customer with username : {costumer}")
            manager_menu(username)
        manager_menu(username)
    elif choice == '9':
        main_menu()
    elif choice == '10':
        my_log.logger.info(f"{username} exited online shop!")
        sys.exit()


def customer_menu(username):
    """
    the customer menu that is printed for user!
    """
    print("=" * 25)
    print('Customer Menu')
    print("""What do you want to do?\n
        1. View previous invoices\n2. Buy Products\n
        3. Back to main menu\n4. Exit\n""")
    print("=" * 25)
    choice = input('What is your choice: \n')
    if choice == '1':
        Customer.view_invoices(username)
        customer_menu(username)
    elif choice == '2':
        shopping(username)
        customer_menu(username)
    elif choice == '3':
        main_menu()
    elif choice == '4':
        my_log.logger.info(f"{username} exited online shop!")
        sys.exit()

    else:
        customer_menu(username)


def shopping(costumer_username_):
    def customer_menu_in_chosen_shop(costumer_username, shop):
        """
        the customer menu that is printed for chosen_shop!
        """
        print("=" * 25)
        print(f"Your chosen shop : {shop}")
        print('1. View list of products')
        print('2. Product search')
        print('3. Add a product to your cart')
        print('4. View invoice before finalizing')
        print('5. Back to last menu')
        print('6. Exit')
        print("=" * 25)
        choice = input("Enter your choice: \n")
        if choice == '1':
            Shop.shop_products(shop)
            customer_menu_in_chosen_shop(costumer_username, shop)
        elif choice == '2':
            product_name = input('Enter the name of product : ')
            product_brand = input('Enter the name of the brand : ')
            Shop.search_product(shop, product_name, product_brand)
            customer_menu_in_chosen_shop(costumer_username, shop)
        elif choice == '3':
            product_name = input('Enter the name of product : ')
            product_brand = input('Enter the brand : ')
            count = input(f'How many {product_name}s do you want? ')
            factored_product = Shop.check_inventory_for_sell(shop, product_name, product_brand, count)
            if factored_product:
                Customer.add_product_to_cart(costumer_username, shop, factored_product)
            customer_menu_in_chosen_shop(costumer_username, shop)
        elif choice == '4':
            cart = Customer.view_invoice_shop_user(costumer_username, shop)
            if cart:
                print("=" * 25)
                print('1. Confirm purchase')
                print('2. Edit purchase')
                print("=" * 25)
                choice = input("Enter your choice: \n")
                if choice == '1':
                    error = Shop.sell_products_shop(shop, costumer_username, cart)
                    if not error:
                        Customer.finalize_cart(costumer_username, shop)
                        my_log.logger.info(f"Costumer with {costumer_username} just purchased in {shop} shop!")
                    else:
                        print(f' Dear {costumer_username}\nWe were unable to finalize your cart!')
                        my_log.logger.info(f"Unable to finalize {costumer_username} cart for {shop} shop!")
                        customer_menu_in_chosen_shop(costumer_username, shop)
                elif choice == '2':
                    cart = Customer.view_invoice_shop_user(costumer_username, shop)
                    Customer.edit_invoice_shop_user(costumer_username, shop)
            else:
                print(f'Dear {costumer_username}\nYour cart is empty!')
                my_log.logger.info(f" {costumer_username} cart in {shop} shop is empty!")
            customer_menu_in_chosen_shop(costumer_username, shop)
        elif choice == '5':
            shopping(costumer_username)
        elif choice == '6':
            my_log.logger.info(f"{costumer_username} exited online shop!")
            sys.exit()

    def customer_menu_before_choosing_shop(costumer_username):
        """
        the customer's menu before choosing any shops
        :param costumer_username: customer's username
        """
        print("=" * 25)
        print("""What do you want to do?\n
            1. View all shops\n2. Search for shops\n
            3. Select a shop\n4. View last invoice\n
            5. Go Back to the last menu\n6. Exit\n""")
        print("=" * 25)
        choice = input('What is your choice: \n')
        if choice == '1':
            Shop.open_shops()
            customer_menu_before_choosing_shop(costumer_username)
        elif choice == '2':
            string = input('Enter the name of the desired shop: ')
            Shop.search_shop(string)
            customer_menu_before_choosing_shop(costumer_username)
        elif choice == '3':
            shop = input('Shop Name: ')
            result = Shop.choose_shop_to_buy(shop, costumer_username)
            if result:
                shop_name = result['Shop Name']
                customer_menu_in_chosen_shop(costumer_username, shop_name)
            customer_menu_before_choosing_shop(costumer_username)
        elif choice == '4':
            Customer.view_invoices(costumer_username)
        elif choice == '5':
            customer_menu(costumer_username)
        elif choice == '6':
            my_log.logger.info(f"{costumer_username} exited online shop!")
            sys.exit()

    customer_menu_before_choosing_shop(costumer_username_)


def register_manager_shop():
    """
    inputs the shop's information and creates the shop
    """
    shop, password = '', ''
    start_work_time = '1'
    end_work_time = '0'
    phone_number = input("Enter your phone number 'Notice that it is gonna be used as your username': ")
    while not validation_phone_number(phone_number):
        print("Wrong phone number!")
        my_log.logger.warning("Wrong phone number was entered as username!")
        phone_number = input("Enter your phone number 'Notice that it is gonna be used as your username': ")
    username = phone_number
    if username_exists(username):
        while not validation_password(password):
            password = input('Enter Password : ')
            rep_pass = input('Repeat password : ')
            if rep_pass != password:
                print('Repeated password does not match!')
                my_log.logger.warning(f"{username} entered wrong repeated password!'")
                while rep_pass != password:
                    password = input('Enter password : ')
                    rep_pass = input('Repeat password : ')
        while not shop:
            shop = input('Shop name : ')
        while not start_work_time or not end_work_time or end_work_time < start_work_time:
            while not validation_time(str(start_work_time)):
                start_work_time = input("Opening time Use  24-hour digital clock with"
                                        " leading zero for hours (hh:mm:ss): ")
            while not validation_time(str(end_work_time)):
                end_work_time = input("Closing time Use  24-hour digital clock with leading zero for "
                                      "hours (hh:mm:ss): ")
        Shop(username, password_hashing(password), shop, start_work_time, end_work_time)
        my_log.logger.info(f"manager with username:{username} has signed up for {shop} shop")
    else:
        print(f'{username} already registered!')
        my_log.logger.info(f'{username} already registered!')


def register_user():
    """
    the register menu that is printed for user!
    """
    print("=" * 25)
    print("What do you want to do?")
    print('1. Shop manager')
    print('2. Customer')
    print('3. Go back to main menu without registering')
    print('4. Exit')
    print("=" * 25)
    choice = input("Enter your choice: \n")
    if choice == '1':
        register_manager_shop()
        main_menu()
    elif choice == '2':
        register_customer()
        main_menu()
    elif choice == '3':
        main_menu()
    elif choice == "4":
        my_log.logger.info("Exited from the main menu!")
        sys.exit()
    else:
        my_log.logger.info("Wrong choice for the main menu!")
        register_user()


def sign_in():
    """
    Inputs information for signing in!
    """
    username = input('Username : ')
    password = input('Password : ')
    user = user_info(username)
    if user:
        if user['password'] == password_hashing(password):
            if user['type'] == 'Customer':
                my_log.logger.info(f"costumer with username:{user['username']} signed in")
                customer_menu(user['username'])
            elif user['type'] == 'Manager':
                try:
                    Shop.shop_inventory_warning(Shop.shop_manager_info(username))
                except TypeError:
                    my_log.logger.exception('error in showing inventory', exc_info=True)
                my_log.logger.info(f"manager with username:{user['username']} signed in")
                manager_menu(Shop.shop_manager_info(username))
        else:
            print('Incorrect password!!')
            my_log.logger.warning(f"username {user['username']} entered an incorrect password to sign in!")
            sign_in()
    else:
        print("Username not found!")
        my_log.logger.warning(f"User tried to sign in with unregistered username: {username}")
        main_menu()


def register_customer():
    """
    inputs the information needed for registering a customer
    """
    first_name = input('First Name: ')
    last_name = input('Last Name: ')
    phone_number = input("Enter your phone number 'Notice that it is gonna be used as your username': ")
    while not validation_phone_number(phone_number):
        print("Wrong phone number!")
        my_log.logger.warning("Wrong phone number was entered as username!")
        phone_number = input("Enter your phone number 'Notice that it is gonna be used as your username': ")
    username = phone_number
    if username_exists(username):
        password = ''
        while not validation_password(password):
            password = input('Enter password : ')
            rep_pass = input('Repeat password : ')
            if rep_pass != password:
                print('Repeated password does not match!')
                my_log.logger.warning(f"{username} entered wrong repeated password!'")
                while rep_pass != password:
                    password = input('Enter password : ')
                    rep_pass = input('Repeat password : ')
        Customer(first_name, last_name, username, password_hashing(password))
        my_log.logger.info(f"Customer with username:{username} was signed up!")
    else:
        print(f'{username} already registered!')
        my_log.logger.info(f'{username} already registered!')


# run
main_menu()
