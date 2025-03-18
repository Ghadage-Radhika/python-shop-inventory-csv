import csv
from tabulate import tabulate

class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

class Inventory:
    def __init__(self, filename='inventory.csv'):
        self.filename = filename
        self.products = self.load_inventory()
    
    def load_inventory(self):
        products = {}
        try:
            with open(self.filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    product_id, name, price, quantity = row
                    products[product_id] = Product(product_id, name, float(price), int(quantity))
        except FileNotFoundError:
            with open(self.filename, mode='w') as file:
                writer = csv.writer(file)
                writer.writerow(["product_id", "product_name", "price", "quantity"])
        return products
    
    def save_inventory(self):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["product_id", "product_name", "price", "quantity"])
            for product in self.products.values():
                writer.writerow([product.product_id, product.name, product.price, product.quantity])
    
    def add_product(self, product):
        if product.product_id in self.products:
            print("Product ID already exists.")
        else:
            self.products[product.product_id] = product
            self.save_inventory()
            print("Product added successfully!")
    
    def update_quantity(self, product_id, quantity):
        if product_id in self.products:
            self.products[product_id].quantity -= quantity
            self.save_inventory()
    
    def display_inventory(self):
        table = [[p.product_id, p.name, p.price, p.quantity] for p in self.products.values()]
        print(tabulate(table, headers=["ID", "Name", "Price", "Stock"], tablefmt="grid"))

class Sale:
    def __init__(self, sale_id):
        self.sale_id = sale_id
        self.items = []
    
    def add_item(self, product, quantity):
        total_price = product.price * quantity
        self.items.append((product.product_id, product.name, quantity, total_price))
    
    def get_total(self):
        return sum(item[3] for item in self.items)

class SalesManager:
    def __init__(self, filename='sales.csv'):
        self.filename = filename
    
    def record_sale(self, sale):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            for item in sale.items:
                writer.writerow([sale.sale_id, *item])
    
    def display_sales(self):
        try:
            with open(self.filename, mode='r') as file:
                reader = csv.reader(file)
                data = list(reader)
                if data:
                    print(tabulate(data, headers=["Sale ID", "Product ID", "Product Name", "Quantity Sold", "Total Price"], tablefmt="grid"))
                else:
                    print("No sales recorded yet.")
        except FileNotFoundError:
            print("Sales file not found.")

class ShopSystem:
    def __init__(self):
        self.inventory = Inventory()
        self.sales_manager = SalesManager()
    
    def run(self):
        while True:
            print("\n--- Small Shop Management System ---")
            print("1. View Inventory")
            print("2. Add Product to Inventory")
            print("3. Process a Sale")
            print("4. View Sales Report")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.inventory.display_inventory()
            elif choice == "2":
                self.add_product()
            elif choice == "3":
                self.process_sale()
            elif choice == "4":
                self.sales_manager.display_sales()
            elif choice == "5":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def add_product(self):
        product_id = input("Enter Product ID: ")
        name = input("Enter Product Name: ")
        price = float(input("Enter Product Price: "))
        quantity = int(input("Enter Product Quantity: "))
        product = Product(product_id, name, price, quantity)
        self.inventory.add_product(product)
    
    def process_sale(self):
        sale_id = input("Enter Sale ID: ")
        sale = Sale(sale_id)
        while True:
            product_id = input("Enter Product ID to sell (or 'done' to finish): ")
            if product_id.lower() == 'done':
                break
            if product_id not in self.inventory.products:
                print("Product not found.")
                continue
            quantity = int(input(f"Enter quantity for {self.inventory.products[product_id].name}: "))
            if quantity > self.inventory.products[product_id].quantity:
                print("Not enough stock available.")
                continue
            sale.add_item(self.inventory.products[product_id], quantity)
            self.inventory.update_quantity(product_id, quantity)
        self.sales_manager.record_sale(sale)
        print(f"Sale {sale_id} recorded successfully.")

if __name__ == "__main__":
    shop = ShopSystem()
    shop.run()
