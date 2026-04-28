
# Simple collaborative filtering (co-occurrence) using purchase history
from collections import defaultdict

class Recommender:
    def __init__(self):
        # co-purchase matrix: item_i -> {item_j: count}
        self.co = defaultdict(lambda: defaultdict(int))

    def fit(self, orders):
        # orders: list of lists of product_ids
        for basket in orders:
            for i in basket:
                for j in basket:
                    if i != j:
                        self.co[i][j] += 1

    def recommend(self, product_id, k=5):
        scores = self.co.get(product_id, {})
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [pid for pid, _ in ranked[:k]]

# Example:
# orders = [[1,2,3],[1,4],[2,3,5]]
# rec = Recommender(); rec.fit(orders); rec.recommend(1)
