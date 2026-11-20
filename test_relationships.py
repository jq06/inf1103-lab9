from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product import Product
from inventory import Inventory
from order import Order


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


print("=== 2. ASSOCIATION ===")
supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 10, 2.1, supplier)
ebook = DigitalProduct("D001", "Python eBook", 25.00, 100, 15.5, supplier)

laptop.supplier.display_information()
ebook.supplier.display_information()
print("Same supplier object:", laptop.supplier is ebook.supplier)

del supplier
print("After del, laptop supplier:", laptop.supplier.name)
print("After del, ebook supplier:", ebook.supplier.name)

print("\n=== 3. AGGREGATION ===")
inv_a, inv_b = Inventory(), Inventory()
inv_a.add_product(laptop)
inv_a.add_product(ebook)

removed = inv_a.remove_product("P001")
print("Removed from A:", removed is laptop)
print("A still has laptop:", inv_a.find_product("P001"))
laptop.update_stock(8)
print("Laptop still usable, stock =", laptop.stock)

inv_b.add_product(laptop)
print("Same object in B:", inv_b.find_product("P001") is laptop)

print("\n=== 4. COMPOSITION ===")
order1, order2 = Order("O001"), Order("O002")
order1.add_order_line(laptop, 2)
order1.add_order_line(ebook, 3)
order2.add_order_line(laptop, 1)

order1.display_order()
order2.display_order()

print("Same Product object in both orders:",
      order1.order_lines[0].product is order2.order_lines[0].product)
print("Different OrderLine objects:",
      order1.order_lines[0] is not order2.order_lines[0])

order1.remove_order_line("D001")
order1.display_order()

print("\n=== 6. LSP: show_product_details ===")
show_product_details(laptop)
print()
show_product_details(ebook)

print("\n=== 7. POLYMORPHISM ===")
inventory = Inventory()
inventory.add_product(laptop)
inventory.add_product(ebook)

for product in inventory.products:
    product.display_information()
    print(product.get_fulfilment_info())
    print("-" * 35)