from product import Product
from discount_strategy import DiscountStrategy, NoDiscount

class OrderLine:

    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display_information(self) -> None:
        print(f"{self.product.name} x {self.quantity} "
              f"@ ${self.product.price:.2f} = ${self.calculate_subtotal():.2f}")


class Order:

    def __init__(self, order_id: str,
                 discount: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = discount or NoDiscount()

    @property
    def order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> None:
        self.__order_lines = [
            line for line in self.__order_lines
            if line.product.product_id != product_id
        ]

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.__order_lines)
        return self.__discount.apply(total)

    def display_order(self) -> None:
        print(f"\nOrder {self.order_id}")
        for line in self.__order_lines:
            line.display_information()
        print(f"Total: ${self.calculate_total():.2f}")