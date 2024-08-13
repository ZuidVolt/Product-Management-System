import unittest
from typing import List, Dict, Any
from unittest.mock import patch
from io import StringIO
from typing import ClassVar
import pathlib

# modules under test
from product_management import ProductManager


class TestProductManager(unittest.TestCase):
    TEST_FILE = "test_products.json"

    product_data: ClassVar[List[Dict[str, Any]]] = [
        {"product_id": 1, "name": "Apple", "price": 10.99, "description": "Fresh apple", "quantity": 50},
        {"product_id": 2, "name": "Banana", "price": 5.99, "description": "Yellow banana", "quantity": 100},
        {"product_id": 3, "name": "Cherry", "price": 20.99, "description": "Red cherry", "quantity": 30},
    ]

    def setUp(self):
        self.pm = ProductManager(self.TEST_FILE)

    def tearDown(self):
        test_file_path = pathlib.Path(self.TEST_FILE)
        if test_file_path.exists():
            test_file_path.unlink()

    def test_init(self):
        self.assertEqual(self.pm.file_name, self.TEST_FILE)
        self.assertEqual(self.pm.products, [])

    def _add_test_product(self, name: str, price: float, description: str, quantity: int) -> Dict[str, Any]:
        with patch("builtins.input", side_effect=[name, str(price), description, str(quantity)]):
            self.pm.add_product()
        return self.pm.products[-1]

    def test_add_product(self):
        product = self._add_test_product("Test Product", 10.99, "Test Description", 5)
        self.assertEqual(len(self.pm.products), 1)
        self.assertEqual(product["name"], "Test Product")
        self.assertEqual(product["price"], 10.99)
        self.assertEqual(product["description"], "Test Description")
        self.assertEqual(product["quantity"], 5)

    def test_remove_product(self):
        self._add_test_product("Test Product", 10.99, "Test Description", 5)
        initial_length = len(self.pm.products)
        self.pm.remove_product(1)
        self.assertEqual(len(self.pm.products), initial_length - 1)

    def test_update_product(self):
        self._add_test_product("Initial Product", 10.99, "Initial Description", 5)
        with patch("builtins.input", side_effect=["Updated Product", "15.99", "Updated Description", "10"]):
            self.pm.update_product(1)
        updated_product = self.pm.products[0]
        self.assertEqual(updated_product["name"], "Updated Product")
        self.assertEqual(updated_product["price"], 15.99)
        self.assertEqual(updated_product["description"], "Updated Description")
        self.assertEqual(updated_product["quantity"], 10)

    def test_sort_products(self):
        self.pm.products = self.product_data

        with patch("builtins.input", return_value="p"):
            self.pm.sort_products()
        self.assertEqual([p["price"] for p in self.pm.products], [5.99, 10.99, 20.99])

        with patch("builtins.input", return_value="n"):
            self.pm.sort_products()
        self.assertEqual([p["name"] for p in self.pm.products], ["Apple", "Banana", "Cherry"])

    def test_search_product(self):
        self.pm.products = self.product_data
        test_cases = [
            ("Apple", "Apple"),
            ("1", "Apple"),  # Search by product_id
            ("Grape", ""),  # No result
        ]

        # Corrected version:
        for search_input, expected_output in test_cases:
            with (
                self.subTest(search_input=search_input),
                patch("builtins.input", return_value=search_input),
                patch("sys.stdout", new=StringIO()) as fake_out,
            ):
                self.pm.search_product()
                self.assertIn(expected_output, fake_out.getvalue())


class TestUserManager(unittest.TestCase):
    """ """

    # Unit tests for UserManager


class TestOrderManager(unittest.TestCase):
    """ """

    # Unit tests for OrderManager


class TestInventoryManager(unittest.TestCase):
    """ """

    # Unit tests for InventoryManager


class TestIntegration(unittest.TestCase):
    """ """

    # Integration tests for the application


if __name__ == "__main__":
    unittest.main()
