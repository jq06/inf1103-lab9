import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from supplier import Supplier
from inventory import Inventory
from order import Order
from discount_strategy import (NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)
from product_factory import ProductFactory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from input_helpers import get_positive_float
from product_loader import load_products


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")

    def make_order_250(self):
        order = Order("O001")
        product = ProductFactory.create("physical", "P001", "Item",
                                        125.0, 10, self.supplier)
        order.add_order_line(product, 2)  # total = 250
        return order


class TestStrategy(BaseTestCase):
    def test_default_is_no_discount(self):
        self.assertEqual(self.make_order_250().calculate_total(), 250)

    def test_bulk_discount(self):
        order = self.make_order_250()
        order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)

    def test_set_discount_changes_strategy(self):
        order = self.make_order_250()
        order.set_discount(BulkDiscount(200, 20))
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225)

    def test_student_discount_needs_no_order_change(self):
        order = self.make_order_250()
        order.set_discount(StudentDiscount())
        self.assertAlmostEqual(order.calculate_total(), 237.5)

    def test_bulk_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(150), 150)

    def test_no_discount(self):
        self.assertEqual(NoDiscount().apply(99), 99)


class TestFactory(BaseTestCase):
    def test_creates_correct_types(self):
        physical = ProductFactory.create("physical", "P1", "A", 5, 1, self.supplier)
        digital = ProductFactory.create("digital", "D1", "B", 5, 1, self.supplier)
        self.assertIsInstance(physical, PhysicalProduct)
        self.assertIsInstance(digital, DigitalProduct)

    def test_unknown_type(self):
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            ProductFactory.create("service", "S1", "C", 5, 1, self.supplier)


class TestValidation(BaseTestCase):
    def test_invalid_price(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P1", "A", 0, 1, self.supplier)

    def test_negative_stock(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D1", "B", 5, -1, self.supplier)

    def test_update_stock_negative(self):
        product = ProductFactory.create("digital", "D1", "B", 5, 1, self.supplier)
        with self.assertRaises(ValueError):
            product.update_stock(-5)

    def test_order_quantity_must_be_positive(self):
        order = Order("O1")
        product = ProductFactory.create("physical", "P1", "A", 5, 1, self.supplier)
        with self.assertRaises(ValueError):
            order.add_order_line(product, 0)


class TestInputHandling(unittest.TestCase):
    def test_get_positive_float_retries(self):
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with redirect_stdout(buffer):
                result = get_positive_float("Price: ")
        self.assertEqual(result, 12.50)
        self.assertIn("valid number", buffer.getvalue())
        self.assertIn("greater than zero", buffer.getvalue())


class TestLoadProducts(BaseTestCase):
    def test_skips_bad_rows(self):
        csv_text = (
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Desk Lamp,25.00,10\n"
            "digital,D001,Photo Editor,49.90,100\n"
            "service,S001,Installation,30.00,5\n"
            "physical,P002,Office Chair,abc,3\n"
            "physical,P003,Monitor Stand,39.50,7\n"
        )
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "products.csv")
            with open(path, "w", newline="") as f:
                f.write(csv_text)

            inventory = Inventory()
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                load_products(path, inventory, self.supplier)

        self.assertEqual(len(inventory.products), 3)
        self.assertIn("3 products loaded.", buffer.getvalue())
        self.assertIn("Load attempt finished.", buffer.getvalue())

    def test_missing_file(self):
        inventory = Inventory()
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            load_products("does_not_exist.csv", inventory, self.supplier)

        self.assertIn("not found", buffer.getvalue())
        self.assertIn("Load attempt finished.", buffer.getvalue())
        self.assertEqual(len(inventory.products), 0)


if __name__ == "__main__":
    unittest.main()