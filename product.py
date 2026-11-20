from abc import ABC, abstractmethod

from supplier import Supplier

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        self.product_id: str = product_id
        self.name: str = name
        self.price: float = price
        self.stock: int = stock
        self.supplier: Supplier = supplier

    def update_stock(self, new_stock: int) -> None:
        self.stock = new_stock

    def display_information(self) -> None:
        print(f"Product ID: {self.product_id}")
        print(f"Product Name: {self.name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Stock Quantity: {self.stock}")
        print(f"Supplier: {self.supplier.name} ({self.supplier.supplier_id})")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass