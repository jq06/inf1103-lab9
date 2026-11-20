from product import Product


class Inventory:

    def __init__(self) -> None:
        self.__products: list[Product] = []

    @property
    def products(self) -> list[Product]:
        return list(self.__products)

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.product_id.lower() == product_id.lower():
                return product
        return None

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)  # drops the reference only
        return product

    def display_all_products(self) -> None:
        print("\nCurrent Inventory")

        if not self.__products:
            print("No products available.")
            return

        for product in self.__products:
            product.display_information()
            print(f"Fulfilment: {product.get_fulfilment_info()}")
            print("-" * 35)