import json
import os

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product import Product
from supplier import Supplier

DEFAULT_SUPPLIER: dict[str, str] = {
    "id": "S000",
    "name": "Unknown Supplier",
    "email": "unknown@example.com",
}


def get_shared_supplier(item: dict, suppliers: dict[str, Supplier]) -> Supplier:
    data = item.get("supplier", DEFAULT_SUPPLIER)
    supplier_id = data["id"]

    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, data["name"], data["email"])

    return suppliers[supplier_id]


def load_inventory() -> Inventory:
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}

    if os.path.exists("inventory.json"):
        print("inventory.json found.")

        try:
            with open("inventory.json", "r") as f:
                data = json.load(f)

            for item in data:
                supplier = get_shared_supplier(item, suppliers)

                if item["type"] == "physical":
                    product = PhysicalProduct(
                        item["id"], item["name"], item["price"],
                        item["stock"], item["weight"], supplier
                    )

                elif item["type"] == "digital":
                    product = DigitalProduct(
                        item["id"], item["name"], item["price"],
                        item["stock"], item["download_size"], supplier
                    )

                else:
                    print("Unknown product type. Product skipped.")
                    continue

                inventory.add_product(product)

            print("Inventory loaded successfully.")

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("Error loading inventory.json, starting with empty inventory.")
            inventory = Inventory()

    else:
        print("inventory.json not found. Starting with empty inventory.")

    return inventory


def base_fields(product: Product) -> dict:
    return {
        "id": product.product_id,
        "name": product.name,
        "price": product.price,
        "stock": product.stock,
        "supplier": {
            "id": product.supplier.supplier_id,
            "name": product.supplier.name,
            "email": product.supplier.contact_email,
        },
    }


def save_inventory(inventory: Inventory) -> None:
    print("\nSaving inventory...")

    data = []

    for product in inventory.products:

        if isinstance(product, PhysicalProduct):
            data.append({"type": "physical", **base_fields(product),
                         "weight": product.weight})

        elif isinstance(product, DigitalProduct):
            data.append({"type": "digital", **base_fields(product),
                         "download_size": product.download_size})

    with open("inventory.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Inventory saved successfully to inventory.json.")