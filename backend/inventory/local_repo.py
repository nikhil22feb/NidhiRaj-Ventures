
# Simple in-memory/local repository example
class LocalRepo:
    def __init__(self):
        self._products = [
            {"sku":"SKU1","stock":50},
            {"sku":"SKU2","stock":30},
        ]

    def get_all_products(self):
        return self._products
