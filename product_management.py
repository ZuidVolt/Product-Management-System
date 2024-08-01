# Handles product-related operations such as adding, removing, updating, sorting, and searching products.
import json


class ProductManager:
    """A class used to manage products."""

    def __init__(self, file_name: str = "products.json"):
        self.file_name = file_name
        self.products: list = []
        self._load_json_file(file_name)

    def _save_to_json_file(self, file_name: str):
        with open(file_name, "w") as file:
            json.dump(self.products, file)

    def _load_json_file(self, file_name):
        try:
            with open(file_name, "r") as file:
                self.products = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.products = []

    def add_product(self):
        """Add a new product to the list."""
        new_product = {
            "product_id": self.get_next_product_id(),
            "name": input("Enter the product name: "),
            "price": float(input("Enter the product price: ")),
            "description": input("Enter the product description: "),
            "quantity": int(input("Enter the product quantity: ")),
        }
        self.products.append(new_product)
        self._save_to_json_file(self.file_name)

    def get_next_product_id(self):
        if not self.products:
            return 1
        else:
            return max(product["product_id"] for product in self.products) + 1

    def remove_product(self, product_id):
        self.products = [product for product in self.products if product["product_id"] != product_id]
        self._save_to_json_file(self.file_name)

    def update_product(self, product_id):
        updated_product = {}
        for product in self.products:
            if product["product_id"] == product_id:
                updated_product["name"] = input("Enter the new name: ")
                updated_product["price"] = str(float(input("Enter the new price: ")))
                updated_product["description"] = input("Enter the new description: ")
                updated_product["quantity"] = str(int(input("Enter the new quantity: ")))
        self.products = [product if product["product_id"] != product_id else updated_product]
        self._save_to_json_file(self.file_name)

    def sort_products(self):
        order = input("Do you want to sort by price (p) or name (n)? ")
        if order.lower() == "p":
            self.products.sort(key=lambda x: x["price"])
        elif order.lower() == "n":
            self.products.sort(key=lambda x: x["name"])

    def search_product(self):
        query = input("Enter the product ID or name to search: ")
        result = [
            product
            for product in self.products
            if product["product_id"] == int(query) or product["name"].lower() == query.lower()
        ]
        print(result)


if __name__ == "__main__":
    # Create an instance of the ProductManager class
    product_manager = ProductManager()

    while True:
        # Display a menu to the user with options to add, remove, update, sort, and search products
        print("\nProduct Manager Menu:")
        print("------------------------")
        print("1. Add product")
        print("2. Remove product")
        print("3. Update product")
        print("4. Sort products by price or name")
        print("5. Search for a product")
        print("6. Exit")

        # Ask the user to enter their choice
        choice = input("Enter your choice: ")

        if choice == "1":
            # If the user chooses to add a product, call the add_product method
            product_manager.add_product()
        elif choice == "2":
            # If the user chooses to remove a product, ask them to enter the product ID and call the remove_product method
            product_id = int(input("Enter the product ID to remove: "))
            product_manager.remove_product(product_id)
        elif choice == "3":
            # If the user chooses to update a product, ask them to enter the product ID and call the update_product method
            product_id = int(input("Enter the product ID to update: "))
            product_manager.update_product(product_id)
        elif choice == "4":
            # If the user chooses to sort products, call the sort_products method
            product_manager.sort_products()
        elif choice == "5":
            # If the user chooses to search for a product, call the search_product method
            product_manager.search_product()
        elif choice == "6":
            # If the user chooses to exit, break out of the loop and end the program
            break
        else:
            # If the user enters an invalid choice, print an error message
            print("Invalid choice. Please try again.")
