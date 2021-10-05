import my_log
from invoice import Invoice
from prettytable import PrettyTable
from File_Handler import UsersFileHandler, CostumerFileHandler


class Customer:
    def __init__(self, first_name, last_name, user_name, password):
        """
        :param first_name: Customer's name
        :param last_name: Customer's last name
        :param user_name: Customer's user name
        :param password: Customer's password

        each customer has a cart and previous invoices as well!
        which are stored in a dictionary and a list.
        """
        self.cart = {}
        self.last_invoices = []
        self.first_name = first_name
        self.last_name = last_name
        self.username = user_name
        self.password = password
        self.add_customer_to_users()

    @staticmethod
    def view_invoices(user_name):
        """
        :param user_name: this function takes a username.
        and shows all the previous invoices if exist.
        """
        customers = CostumerFileHandler().read()
        customer = customers[user_name]
        list_invoices = customer['last_invoices']
        if list_invoices:
            pretty_table(list_invoices)
        else:
            my_log.logger.info(f"The {user_name}'s invoice list is empty!")
            my_log.logger.warning("No Such File or Directory as invoices.txt")

    @staticmethod
    def add_product_to_cart(user_name, shop, product):
        """
        this function takes a username and a product from a special shop and adds that product
        to the users cart!
        :param user_name: customer's username
        :param shop: name of the shop
        :param product: the product that customer wants to buy
        """
        costumers = CostumerFileHandler().read()
        costumer = costumers[user_name]
        cart = costumer['cart']
        if shop in list(cart.keys()):
            cart[shop].append(product)
        else:
            cart[shop] = []
            cart[shop].append(product)
        CostumerFileHandler().update(costumers)

    @staticmethod
    def view_invoice_shop_user(user_name, shop):
        """
        :param user_name: customers username
        :param shop: name of the shop
        :return: the cart of the user in that specific shop
        """
        costumers = CostumerFileHandler().read()
        costumer = costumers[user_name]
        cart = costumer["cart"][shop]
        if cart != [None] and cart != []:
            pretty_table(cart)
            return cart

    @staticmethod
    def edit_invoice_shop_user(user_name, shop):
        """
        this function gives the user the ability of editing the cart of a specific shop
        number of each item in cart can be edited by entering a new int or can be deleted
        by entering 'del' otherwise you can press enter if you want to pass that item
        :param user_name: customer's username
        :param shop: name of the shop
        """
        costumers = CostumerFileHandler().read()
        costumer = costumers[user_name]
        cart = costumer["cart"][shop]
        for num, item in enumerate(cart):
            pretty_table([item])
            choice = input(f"Dear {user_name} you are editing yor cart from {shop}:\n"
                           f"1. Edit the number of the product by writing a number > zero!\n"
                           f"2. Delete the product from your cart!\n"
                           f"Or\n"
                           f"You can press 'Enter' if you want to remain the product unchanged!"
                           )
            if choice:
                if choice == '1':
                    number = input("the number of the product: ")
                    if number.isdigit():
                        if int(number) > 0:
                            item["count"] = number
                            item["price"] = int(number) * int(item["single_price"])
                        else:
                            my_log.logger.info(f"{user_name} entered a number which was not greater than zero for"
                                               f"editing cart in {shop} shop")
                elif choice == '2':
                    cart.pop(num)
        CostumerFileHandler().update(costumers)

    @classmethod
    def finalize_cart(cls, user_name, shop):
        """
        This function takes a username and a shops name and finds customer's cart in shop and turns that to an
        invoice and empties the customers cart in that shop!
        :param user_name: customer's username
        :param shop: name of the shop
        """
        costumers = CostumerFileHandler().read()
        costumer = costumers[user_name]
        cart = costumer["cart"][shop]
        invoice = Invoice(shop, user_name, cart)
        invoices = costumers[user_name]["last_invoices"]
        costumer["cart"][shop] = []
        invoices.append(invoice.__dict__)
        CostumerFileHandler().update(costumers)

    def add_customer_to_users(self):
        user = UsersFileHandler()
        user.add_to_file({'username': self.username, 'password': self.password, 'type': 'Customer'})
        file_info = CostumerFileHandler()
        file_info.add_to_file(self.__dict__)
        my_log.logger.info(f"customer with username: {self.username} added to the users.")


def pretty_table(dictionaries_list):
    """
    Using pretty table to have a beautiful output!
    """
    table = PrettyTable()
    table.field_names = list(dictionaries_list[0].keys())
    list1 = []
    for item in dictionaries_list:
        list1.append(list(item.values()))
    table.add_rows(list1)
    print(table)


def pretty_invoice(dictionaries_list):
    """
        Using pretty table to have a beautiful output!
    """
    dictionary = dictionaries_list[0]
    inv_table = PrettyTable()
    rows = PrettyTable()
    products = dictionary["products"]
    rows.field_names = ["products_name", "brand", "single_price", "count", "price"]
    a_row = []
    for item in products:
        a_row.append([item["product"], item["brand"], item["single_price"], item["count"], item["price"]])
    rows.add_rows(a_row)
    inv_table.field_names = ["Shop's name", "Costumer", "date", "total price", "products"]
    inv_table.add_row([dictionary["shop"], dictionary["costumer_phone"], dictionary["date"], dictionary["total_price"],
                       rows])
    print(inv_table)
