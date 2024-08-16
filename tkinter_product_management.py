import json
import pathlib
import tkinter as tk
from tkinter import messagebox, simpledialog


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
        name = simpledialog.askstring("Input", "Enter the product name:")
        price = simpledialog.askfloat("Input", "Enter the product price:")
        description = simpledialog.askstring("Input", "Enter the product description:")
        quantity = simpledialog.askinteger("Input", "Enter the product quantity:")

        return {
            "name": name,
            "price": price,
            "description": description,
            "quantity": quantity,
        }

    def add_product(self):
        """Add a new product to the list."""
        new_product = {
            "product_id": self.get_next_product_id(),
            **self._get_product_input(),
        }
        self.products.append(new_product)
        self._save_to_json_file(self.file_name)
        messagebox.showinfo("Success", "Product added successfully!")

    def get_next_product_id(self):
        return max((product["product_id"] for product in self.products), default=0) + 1

    def remove_product(self, product_id):
        self.products = [product for product in self.products if product["product_id"] != product_id]
        self._save_to_json_file(self.file_name)
        messagebox.showinfo("Success", "Product removed successfully!")

    def update_product(self, product_id):
        for product in self.products:
            if product["product_id"] == product_id:
                updated_product = self._get_product_input()
                product.update(updated_product)
                break
        self._save_to_json_file(self.file_name)
        messagebox.showinfo("Success", "Product updated successfully!")

    def sort_products(self):
        order = simpledialog.askstring("Sort", "Do you want to sort by price (p) or name (n)?")
        if order is not None:
            order = order.lower()
            if order == "p":
                self.products.sort(key=lambda x: x["price"])
            elif order == "n":
                self.products.sort(key=lambda x: x["name"])
        messagebox.showinfo("Success", f"Products sorted by {'price' if order == 'p' else 'name'}.")

    def search_product(self):
        query = simpledialog.askstring("Search", "Enter the product ID or name to search:")
        if query is not None:
            query = query.lower()
        result = [
            product
            for product in self.products
            if str(product["product_id"]) == query or product["name"].lower() == query
        ]
        if result:
            messagebox.showinfo("Search Result", f"Found products: {result}")
        else:
            messagebox.showinfo("Search Result", "No matching products found.")


def validate_product_id(product_manager: ProductManager, product_id: int) -> bool:
    return any(product["product_id"] == product_id for product in product_manager.products)


def handle_remove_product(product_manager: ProductManager):
    product_id = simpledialog.askinteger("Remove Product", "Enter the product ID to remove:")
    if product_id is not None:
        if validate_product_id(product_manager, product_id):
            product_manager.remove_product(product_id)
        else:
            messagebox.showwarning("Error", "Product ID not found.")


def handle_update_product(product_manager: ProductManager):
    product_id = simpledialog.askinteger("Update Product", "Enter the product ID to update:")
    if product_id is not None:
        if validate_product_id(product_manager, product_id):
            product_manager.update_product(product_id)
        else:
            messagebox.showwarning("Error", "Product ID not found.")


def handle_user_choice(product_manager: ProductManager, choice: str, root: tk.Tk):
    if choice == "1":
        product_manager.add_product()
    elif choice == "2":
        handle_remove_product(product_manager)
    elif choice == "3":
        handle_update_product(product_manager)
    elif choice == "4":
        product_manager.sort_products()
    elif choice == "5":
        product_manager.search_product()
    elif choice == "6" or choice == "q":
        root.quit()


def main():
    product_manager = ProductManager()

    root = tk.Tk()
    root.title("Product Manager")

    # Menu options
    menu_label = tk.Label(root, text="Product Manager Menu", font=("Arial", 14))
    menu_label.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(fill="both", expand=True)
    tk.Button(
        button_frame,
        text="1. Add product",
        command=lambda: handle_user_choice(product_manager, "1", root),
    ).pack(fill="x")

    tk.Button(
        button_frame,
        text="2. Remove product",
        command=lambda: handle_user_choice(product_manager, "2", root),
    ).pack(fill="x")

    tk.Button(
        button_frame,
        text="3. Update product",
        command=lambda: handle_user_choice(product_manager, "3", root),
    ).pack(fill="x")

    tk.Button(
        button_frame,
        text="4. Sort products by price or name",
        command=lambda: handle_user_choice(product_manager, "4", root),
    ).pack(fill="x")

    tk.Button(
        button_frame,
        text="5. Search for a product",
        command=lambda: handle_user_choice(product_manager, "5", root),
    ).pack(fill="x")

    tk.Button(
        button_frame,
        text="6. Exit",
        command=lambda: handle_user_choice(product_manager, "6", root),
    ).pack(fill="x")

    root.mainloop()


if __name__ == "__main__":
    main()
