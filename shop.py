import my_log
import datetime
from invoice import Invoice
from product import Product
from prettytable import PrettyTable
from customer import pretty_table, pretty_invoice
from File_Handler import UsersFileHandler, FileHandler


class Shop:
    def __init__(self, user_name, password, shop, start_work_time, end_work_time):
        self.costumers = []
        self.block_customers = []
        self.products = []
        self.invoices = []
        self.username = user_name
        self.password = password
        self.shop = shop
        self.start = start_work_time
        self.end = end_work_time
        self.add_manager_to_users()

    @staticmethod
    def open_shops():
        """
        check and see if stores are open
        """
        shops = FileHandler().read()
        now = datetime.datetime.now()
        now = datetime.time(now.hour, now.minute, now.second)
        open_shops = []
        for shop in shops.keys():
            store_opening = shops[shop]['start']
            store_closing = shops[shop]['end']
            if store_opening <= str(now) < store_closing:
                open_shops.append(
                    {'Shop Name': shops[shop]['shop'],
                     'Start Working': shops[shop]['start'], 'End Working': shops[shop]['end']})
        if open_shops:
            pretty_table(open_shops)

    @staticmethod
    def add_product_to_shop(shop, name_of_product, brand, product_inventory, product_price, serial, expiration_date):
        """
        this function adds a product to a specific shop
        :param shop: name of the shop
        :param name_of_product: name of the product
        :param brand: brand of the product
        :param product_inventory: number of that specific product to sell
        :param product_price: the price of product
        :param serial: serial of a product or can even be considered as barcode as well
        :param expiration_date: expiration_date of the product
        """
        product = Product(name_of_product, brand, product_inventory, product_price, serial, expiration_date)
        shops = FileHandler().read()
        products_file = shops[shop]["products"]
        products_file.append(product.__dict__)
        FileHandler().update(shops)

    @staticmethod
    def shop_products(shop):
        """
        this function shows the list of products of given shop
        :param shop: name of the shop
        """
        products = FileHandler().read()[shop]["products"]
        if products:
            pretty_table(products)
        else:
            my_log.logger.info(f"{shop} is currently empty and got no product for sell!")
            my_log.logger.warning("No Such File or Directory as products.txt")

    @staticmethod
    def block_customer(shop, costumer_phone_number):
        """
        block a customer with the specific username for the given shop
        if the customer is not already blocked
        :param shop: name of the shop
        :param costumer_phone_number: customers username
        """
        shops = FileHandler().read()
        block_costumers = shops[shop]['block_customers']
        customers = shops[shop]['costumers']
        if costumer_phone_number in customers \
                and costumer_phone_number not in block_costumers:
            block_costumers.append(costumer_phone_number)
            FileHandler().update(shops)
            my_log.logger.info(f"{shop} shop just blocked customer with username: {costumer_phone_number}!")
        else:
            print(f"{costumer_phone_number} is already blocked!")
            my_log.logger.info(f"{shop} tried to block username: {costumer_phone_number} which was blocked already!")

    @staticmethod
    def shop_inventory_warning(shop):
        """
        checks the inventory number of each product in a shop
        :param shop: name of the shop
        """
        products = FileHandler().read()[shop]["products"]
        if products:
            list_of_warning_product = []
            for item in products:
                if int(item['product_count']) <= 5:
                    list_of_warning_product.append(item)
                    my_log.logger.warning(f"{shop} is running out of {item}")
            if list_of_warning_product:
                Shop.warning_product_pretty(list_of_warning_product)
            else:
                my_log.logger.info(f"{shop} you do not have any inventory crisis!")
        else:
            my_log.logger.warning(f"There are no products in {shop} shop to check!")
            my_log.logger.warning("No Such File or Directory as products.txt")

    @staticmethod
    def shop_invoices(shop):
        """
        This functions takes a shop's name as input and shows all invoices of this shop if available!
        :param shop: name of the shop
        """
        invoices = FileHandler().read()[shop]['invoices']
        if invoices:
            for item in invoices:
                pretty_invoice([item])
            my_log.logger.info(f"The {shop}'s invoice list was printed!")
        else:
            my_log.logger.info(f"The {shop}'s invoice list is empty!")
            my_log.logger.warning("No Such File or Directory as invoices.txt")

    @staticmethod
    def warning_product_pretty(list_of_warning_product):
        """
        using pretty table to have an organized output for the products that need warnings!
        :param list_of_warning_product: list of products that a shop is running out of and needs to receive a warning!
        """
        x = PrettyTable()
        x.field_names = list_of_warning_product[0].keys()
        for item in list_of_warning_product:
            x.add_row(item.values())
        print("This products are out of range: ")
        print(x)
        print()

    @staticmethod
    def check_inventory_for_sell(shop, product_name, brand, quantity):
        """
        this function is needed to check the quantity with product's inventory in given shop
        :param shop: name of the shop
        :param product_name: name of the product
        :param brand: name of the brand
        :param quantity: number/quantity of given product in shop
        """
        products = FileHandler().read()[shop]['products']
        product = {}
        replaced_product = {}
        for item in products:
            if product_name == item["product_name"] and brand == item["brand"]:
                product = item
                my_log.logger.info(f"Inventory check: {product_name} with brand {brand} is available in {shop}!")
                break
        if product:
            if int(quantity) <= int(product['product_count']):
                replaced_product['product'] = product['product_name']
                replaced_product['brand'] = product['brand']
                replaced_product['single_price'] = product['product_price']
                replaced_product['count'] = quantity
                replaced_product['price'] = int(quantity) * int(product['product_price'])
                return replaced_product
        else:
            print(f"product was not available with given quantity in {shop}!")
            my_log.logger.warning(f"product was not available with given quantity in {shop}!")

    @staticmethod
    def search_invoices_by_phone_number(customer_phone_number, invoices):
        """
        this function search for an specific user's invoices!
        :param customer_phone_number: the customer's phone number / username that it's invoices are being searched
        :param invoices: all available invoices
        :return: list of founded invoices, if not just the invoices
        """
        founded_invoices = []
        if customer_phone_number:
            for invoice in invoices:
                if customer_phone_number in invoice['costumer_phone']:
                    founded_invoices.append(invoice)
            return founded_invoices
        else:
            my_log.logger.info(f"Unable to find invoices for the given phone number! {customer_phone_number}!")
            return invoices

    @staticmethod
    def search_invoices_by_desired_date(desired_date, invoices):
        """
        this function search for an specific user's invoices!
        :param desired_date: the desired date of invoice in which the invoices has take place
        :param invoices: all available invoices
        :return: list of founded invoices, if not just the invoices
        """
        founded_invoices = []
        if desired_date:
            for invoice in invoices:
                if invoice['date'] == desired_date:
                    founded_invoices.append(invoice)
            return founded_invoices
        else:
            my_log.logger.info(f"Unable to find invoices for the given date! {desired_date}!")
            return invoices

    @staticmethod
    def search_invoices_by_interval_date(interval_date, invoices):
        """
        this function finds all invoices that has been done before the given interval date
        :param interval_date: the desired date of invoice in which the invoices has to be finished before
        :param invoices: all available invoices
        :return: list of founded invoices, if not just the invoices
        """
        founded_invoices = []
        if interval_date:
            for invoice in invoices:
                if invoice['date'] <= interval_date:
                    founded_invoices.append(invoice)
            return founded_invoices
        else:
            my_log.logger.info(f"Unable to find invoices before the given date! {interval_date}!")
            return invoices

    @staticmethod
    def search_shop_invoice(shop, customer_phone_number='', desired_date='', interval_date=''):
        """
        search for a given shop's invoices based on customer's username, date of invoice or before the given date.
        :param shop: name of the shop
        :param customer_phone_number: customer's phone number/username
        :param desired_date: date which invoice has taken place
        :param interval_date: interval given to find invoices before that
        """
        shop_invoices = FileHandler().read()[shop]['invoices']
        if desired_date:
            invoices = Shop.search_invoices_by_desired_date(desired_date,
                                                            Shop.search_invoices_by_phone_number(customer_phone_number,
                                                                                                 shop_invoices))
        else:
            invoices = Shop.search_invoices_by_interval_date(interval_date,
                                                             Shop.search_invoices_by_phone_number(customer_phone_number,
                                                                                                  shop_invoices))
        if invoices:
            [pretty_table([item]) for item in invoices]
            my_log.logger.info(f"Invoices found for {shop_invoices}! based on username: {customer_phone_number},"
                               f"desired date: {desired_date}, given interval: {interval_date}!")
        else:
            print("No invoices were found with given conditions!")
            my_log.logger.warning(f"No invoices were found with given conditions for {shop}")

    @staticmethod
    def pretty_customer(customers):
        """
        using pretty table for printing customers of a shop in an organized way!
        """
        table = PrettyTable(['#', 'costumers PhoneNumber'])
        rows = []
        for i, item in enumerate(customers, start=1):
            rows.append([i, item])
        table.add_rows(rows)
        print(table)
        return True

    @staticmethod
    def shop_customer_list(shop):
        """
        prints the customers of a given shop!
        :param shop: name of the shop
        """
        customers = FileHandler().read()[shop]['costumers']
        if customers:
            Shop.pretty_customer(customers)
            my_log.logger.info(f"Printed list of customers for {shop}!")
        else:
            print(f"{shop} currently has no costumers!")
            my_log.logger.warning("No such file or directory as customers")

    @staticmethod
    def shop_customers_info(shop):
        """
        prints the information about customers of a given shop!
        :param shop: name of the shop
        """
        shops = FileHandler().read()
        customers = shops[shop]['costumers']
        invoices = shops[shop]['invoices']
        if customers:
            for num, customer in enumerate(customers, start=1):
                print(f"{num}. Customer Phone_Number: {customer}")
                for invoice in invoices:
                    if invoice['costumer_phone'] == customer:
                        pretty_invoice([invoice])
                print()
            my_log.logger.info(f"Printed list of customers information for {shop}!")
        else:
            print(f"{shop} currently has no costumers!")
            my_log.logger.warning("No such file or directory as customers")

    @staticmethod
    def search_product(shop, product_name="", brand=""):
        """
        searching for a product in given shop by name and brand
        :param shop: name of the shop
        :param product_name: name of the product
        :param brand: brand of the product
        """
        products = FileHandler().read()[shop]['products']
        found_products = []
        for product in products:
            if product_name == product["product_name"] and brand == product["brand"]:
                found_products.append(product)
        if found_products:
            pretty_table(found_products)
            my_log.logger.info(f"{product_name} was founded in {shop}!")
            return True
        else:
            print(f"No products were found with given conditions in {shop}!")
            my_log.logger.warning(f"No invoices were found with given conditions for {shop}")

    @staticmethod
    def choose_shop_to_buy(shop, customer_username):
        """
        customer chooses an specific shop to buy products from
        :param shop: name of the shop
        :param customer_username: customer's username
        """
        shops = FileHandler().read()
        if shop in shops.keys():
            if customer_username not in shops[shop]['block_customers']:
                chosen = {"Shop Name": shops[shop]['shop'],
                          'Start Working': shops[shop]['start'],
                          'End Working': shops[shop]['end']}
                return chosen
            else:
                print(f"Dear {customer_username} you are blocked by {shop}")
                my_log.logger.warning(f"Blocked customer {customer_username} tried to by from {shop} shop!")
                return False
        print(f"Dear {customer_username} currently there's no shops with name {shop} available!")
        my_log.logger.warning(f"customer {customer_username} tried to by from {shop} shop which does not exists!")
        return False

    @staticmethod
    def sell_products_shop(shop, costumer_phone_number, cart):
        """
        this function sells the products in cart to the customer if the inventory is ok
        :param shop: name of the shop
        :param costumer_phone_number: customer's username
        :param cart: cart which includes the list of products that a customer wants to buy
        """
        shops = FileHandler().read()
        shop_info = shops[shop]

        def update_inventory(customer_cart):
            """
            this function checks the inventory before finalizing the shopping
            if a product's inventory in less than what is needed it is gonna tell the user
            if the inventory is ok it is gonna updated the number of product
            :param customer_cart: cart of the customer
            """
            products_list = shop_info['products']
            can_not_sell = False
            for item in customer_cart:
                quantity, product_name, brand = item['count'], item['product'], item['brand']
                for product in products_list:
                    if product_name == product["product_name"] and brand == product["brand"]:
                        if int(product['product_count']) < int(quantity):
                            print(f"{product_name}'s inventory is less than your needed quantity")
                            my_log.logger.warning(f"{product_name}'s inventory is less than customer's needed"
                                                  f" quantity in {shop}")
                            can_not_sell = True
            if not can_not_sell:
                for item in customer_cart:
                    quantity, product_name, brand = item['count'], item['product'], item['brand']
                    for product in products_list:
                        if product_name == product["product_name"] and brand == product["brand"]:
                            product['product_count'] = int(product['product_count']) - int(quantity)
                            if product['product_count'] == 0:
                                print(f"{product_name} with brand {brand} SOLD OUT!!")
                                my_log.logger.warning(f"{product_name}'s inventory is zero in {shop}")

                invoice = Invoice(shop, costumer_phone_number, customer_cart)
                my_log.logger.info(f"{costumer_phone_number}'s invoice in {shop} produced!")
                shop_info['invoices'].append(invoice.__dict__)
                if costumer_phone_number not in shop_info['costumers']:
                    shop_info['costumers'].append(costumer_phone_number)
                    my_log.logger.info(f"{costumer_phone_number} added to list of customers in {shop} shop!")
                FileHandler().update(shops)
                return True

        update_inventory(cart)

    @staticmethod
    def search_shop(name):
        """
        search for shops with given name and prints information of them
        """
        shops = FileHandler().read()
        found_shops = []
        for shop in shops.keys():
            if name in shop:
                found_shops.append({"Shop's Name": shops[shop]['shop'],
                                    'Start Working': shops[shop]['start'],
                                    'End Working': shops[shop]['end']})
        if found_shops:
            pretty_table(found_shops)
            my_log.logger.info(f"printed shops with '{name}'!")
            return found_shops

    @staticmethod
    def shop_manager_info(manager_username):
        """
        returning the name of the shop which manger works in
        :param manager_username: manager's username
        """
        shops = FileHandler().read()
        for item in shops.keys():
            if manager_username == shops[item]['username']:
                shop = shops[item]['shop']
                return shop

    def add_manager_to_users(self):
        user = UsersFileHandler()
        user.add_to_file({'username': self.username, 'password': self.password, 'type': 'Manager'})
        file_info = FileHandler()
        file_info.add_to_file(self.__dict__)
        my_log.logger.info(f"manager with username: {self.username} added to the users.")


def check_active_user(user_name, customers):
    for customer in customers:
        if customer['username'] == user_name and customer['status'] == 'active':
            return True
