import json
import pathlib


class ProductManager:
    """A class used to manage products."""

    def __init__(self, file_name: str = "products.json"):
        self.file_name = file_name
        self.products: list = []
        self._load_json_file(file_name)

    def _save_to_json_file(self, file_name: str):
        file_path = pathlib.Path(file_name)
        with file_path.open("w") as file:
            json.dump(self.products, file)

    def _load_json_file(self, file_name):
        file_path = pathlib.Path(file_name)
        try:
            with file_path.open() as file:
                self.products = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.products = []

    def _get_product_input(self):
        """Helper method to get product details from the user."""
        return {
            "name": input("Enter the product name: "),
            "price": float(input("Enter the product price: ")),
            "description": input("Enter the product description: "),
            "quantity": int(input("Enter the product quantity: ")),
        }

    def add_product(self):
        """Add a new product to the list."""
        new_product = {
            "product_id": self.get_next_product_id(),
            **self._get_product_input(),
        }
        self.products.append(new_product)
        self._save_to_json_file(self.file_name)

    def get_next_product_id(self):
        return max((product["product_id"] for product in self.products), default=0) + 1

    def remove_product(self, product_id):
        self.products = [product for product in self.products if product["product_id"] != product_id]
        self._save_to_json_file(self.file_name)

    def update_product(self, product_id):
        for product in self.products:
            if product["product_id"] == product_id:
                updated_product = self._get_product_input()
                product.update(updated_product)
                break
        self._save_to_json_file(self.file_name)

    def sort_products(self):
        order = input("Do you want to sort by price (p) or name (n)? ").lower()
        if order == "p":
            self.products.sort(key=lambda x: x["price"])
        elif order == "n":
            self.products.sort(key=lambda x: x["name"])

    def search_product(self):
        query = input("Enter the product ID or name to search: ").strip()
        result = [
            product
            for product in self.products
            if str(product["product_id"]) == query or product["name"].lower() == query.lower()
        ]
        print(result)


if __name__ == "__main__":
    product_manager = ProductManager()

    while True:
        print("\nProduct Manager Menu:")
        print("------------------------")
        print("1. Add product")
        print("2. Remove product")
        print("3. Update product")
        print("4. Sort products by price or name")
        print("5. Search for a product")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            product_manager.add_product()
        elif choice == "2":
            product_id = int(input("Enter the product ID to remove: "))
            product_manager.remove_product(product_id)
        elif choice == "3":
            product_id = int(input("Enter the product ID to update: "))
            product_manager.update_product(product_id)
        elif choice == "4":
            product_manager.sort_products()
        elif choice == "5":
            product_manager.search_product()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")
