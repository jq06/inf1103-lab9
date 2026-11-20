from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        self.product_id: str = product_id
        self.name: str = name
        self.price = price      # goes through the setter (validated)
        self.stock = stock      # goes through the setter (validated)
        self.supplier: Supplier = supplier

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Price must be greater than zero.")
        self.__price = value

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, value: int) -> None:
        if value < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__stock = value

    def update_stock(self, new_stock: int) -> None:
        self.stock = new_stock  # reuses the validated setter

    def display_information(self) -> None:
        print(f"Product ID: {self.product_id}")
        print(f"Product Name: {self.name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Stock Quantity: {self.stock}")
        print(f"Supplier: {self.supplier.name} ({self.supplier.supplier_id})")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass