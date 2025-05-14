import json
from abc import ABC, abstractmethod
from datetime import datetime

class InventoryError(Exception):
    pass

class DuplicateProductError(InventoryError):
    pass

class OutOfStockError(InventoryError):
    pass

class InvalidProductDataError(InventoryError):
    pass

#ABSTRACTION

class Product(ABC):
    def __init__(self, product_id, name, price, quantity_in_stock):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_in_stock = quantity_in_stock

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    def restock(self, amount):
        if amount > 0:
            self._quantity_in_stock += amount

    def sell(self, quantity):
        if quantity <= self._quantity_in_stock:
            self._quantity_in_stock -= quantity
        else:
            raise OutOfStockError(f"Not enough stock for {self._name}")

    def get_total_value(self):
        return self._price * self._quantity_in_stock
#SUBCLASS

class Electronics(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, brand, warranty_years):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._brand = brand
        self._warranty_years = warranty_years

    def __str__(self):
        return (f"[Electronics] {self._name} ({self._brand}) - ${self._price} x {self._quantity_in_stock} "
                f"(Warranty: {self._warranty_years} years)")

    def to_dict(self):
        return {
            "type": "Electronics",
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity_in_stock": self._quantity_in_stock,
            "brand": self._brand,
            "warranty_years": self._warranty_years
        }


class Grocery(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, expiry_date):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._expiry_date = expiry_date  # YYYY-MM-DD format

    def __str__(self):
        status = "Expired" if self.is_expired() else "Valid"
        return (f"[Grocery] {self._name} - ${self._price} x {self._quantity_in_stock} "
                f"(Expires: {self._expiry_date} - {status})")

    def to_dict(self):
        return {
            "type": "Grocery",
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity_in_stock": self._quantity_in_stock,
            "expiry_date": self._expiry_date
        }

    def is_expired(self):
        today = datetime.today().date()
        expiry = datetime.strptime(self._expiry_date, "%Y-%m-%d").date()
        return today > expiry


class Clothing(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, size, material):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._size = size
        self._material = material

    def __str__(self):
        return (f"[Clothing] {self._name} - ${self._price} x {self._quantity_in_stock} "
                f"(Size: {self._size}, Material: {self._material})")

    def to_dict(self):
        return {
            "type": "Clothing",
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity_in_stock": self._quantity_in_stock,
            "size": self._size,
            "material": self._material
        }


#INVENTORY

class Inventory:
    def __init__(self):
        self._products = {}

    def add_product(self, product):
        if product._product_id in self._products:
            raise DuplicateProductError(f"Product with ID {product._product_id} already exists.")
        self._products[product._product_id] = product

    def remove_product(self, product_id):
        if product_id in self._products:
            del self._products[product_id]

    def search_by_name(self, name):
        return [p for p in self._products.values() if name.lower() in p._name.lower()]

    def search_by_type(self, product_type):
        return [p for p in self._products.values() if p.__class__.__name__.lower() == product_type.lower()]

    def list_all_products(self):
        return list(self._products.values())

    def sell_product(self, product_id, quantity):
        if product_id in self._products:
            self._products[product_id].sell(quantity)
        else:
            raise InventoryError(f"No product with ID {product_id}")

    def restock_product(self, product_id, quantity):
        if product_id in self._products:
            self._products[product_id].restock(quantity)

    def total_inventory_value(self):
        return sum(p.get_total_value() for p in self._products.values())

    def remove_expired_products(self):
        to_remove = [pid for pid, p in self._products.items() if isinstance(p, Grocery) and p.is_expired()]
        for pid in to_remove:
            del self._products[pid]

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump([p.to_dict() for p in self._products.values()], f, indent=4)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                for item in data:
                    product_type = item.get("type")
                    if product_type == "Electronics":
                        product = Electronics(**item)
                    elif product_type == "Grocery":
                        product = Grocery(**item)
                    elif product_type == "Clothing":
                        product = Clothing(**item)
                    else:
                        raise InvalidProductDataError("Unknown product type in file.")
                    self.add_product(product)
        except (json.JSONDecodeError, KeyError) as e:
            raise InvalidProductDataError("Invalid product data in file.") from e

def main():
    inventory = Inventory()

    while True:
        print("\n--- Inventory Management System ---")

        print("1. Add Product")
        print("2. Sell Product")
        print("3. Search Product by Name")
        print("4. List All Products")
        print("5. Save Inventory to File")
        print("6. Load Inventory from File")
        print("7. Remove Expired Products")
        print("8. Exit")

        choice = input("Select an option: ")

     
        try:
            if choice == "1":
                print("Select Product Type: 1) Electronics 2) Grocery 3) Clothing")
                ptype = input("Choice: ")
                pid = input("Product ID: ")
                name = input("Name: ")
                price = float(input("Price: "))
                stock = int(input("Quantity in Stock: "))
                if ptype == "1":
                    brand = input("Brand: ")
                    warranty = int(input("Warranty Years: "))
                    product = Electronics(pid, name, price, stock, brand, warranty)
                elif ptype == "2":
                    expiry = input("Expiry Date (YYYY-MM-DD): ")
                    product = Grocery(pid, name, price, stock, expiry)
                elif ptype == "3":
                    size = input("Size: ")
                    material = input("Material: ")
                    product = Clothing(pid, name, price, stock, size, material)
                else:
                    print("Invalid type.")
                    continue
                inventory.add_product(product)
                print("✅Product added successfully.")

            elif choice == "2":
                pid = input("Product ID: ")
                quantity = int(input("Quantity to Sell: "))
                inventory.sell_product(pid, quantity)
                print("✅Product sold successfully.")

            elif choice == "3":
                name = input("Enter name to search: ")
                results = inventory.search_by_name(name)
                for p in results:
                    print(p)

            elif choice == "4":
                for p in inventory.list_all_products():
                    print(p)

            elif choice == "5":
                filename = input("Filename to save (e.g., inventory.json): ")
                inventory.save_to_file(filename)
                print("✅Inventory saved successfully.")

            elif choice == "6":
                filename = input("Filename to load (e.g., inventory.json): ")
                inventory.load_from_file(filename)
                print("✅Inventory loaded successfully.")

            elif choice == "7":
                inventory.remove_expired_products()
                print("Expired products removed.")

            elif choice == "8":
                print("Exiting system...")
                break

            else:
                print("Invalid option.")

       except InventoryError as e:
            print(f"[⚠️Upppsss Error]: {e}")

       except Exception as e:
            print(f"[❌Something wrong!]: {e}")


if __name__ == "__main__":
    main()
