from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier

class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, weight: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.weight: float = weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.weight} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return 2.50 + (self.weight * 1.20)