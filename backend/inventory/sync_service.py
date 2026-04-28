
# Sync inventory between local DB and marketplaces (Amazon/Meesho stubs)
import time

class InventorySyncService:
    def __init__(self, local_repo, amazon_client=None, meesho_client=None):
        self.local_repo = local_repo
        self.amazon = amazon_client
        self.meesho = meesho_client

    def sync_once(self):
        products = self.local_repo.get_all_products()
        for p in products:
            sku = p.get("sku")
            qty = p.get("stock")
            if self.amazon:
                self.amazon.update_inventory(sku, qty)
            if self.meesho:
                # implement meesho client similarly
                print(f"[MEESHO] Update {sku} -> {qty}")

    def run_forever(self, interval_sec=300):
        while True:
            self.sync_once()
            time.sleep(interval_sec)
