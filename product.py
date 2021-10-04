class Product:
    def __init__(self, name_of_product, brand, product_inventory, product_price, serial, expiration_date):
        self.product_name = name_of_product
        self.brand = brand
        self.product_count = product_inventory
        self.product_price = product_price
        self.barcode = serial
        self.expiration_date = expiration_date
