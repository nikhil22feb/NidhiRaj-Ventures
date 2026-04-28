
# Pipeline to update model from real purchase data
from .recommender import Recommender

def build_model(order_repo):
    orders = order_repo.fetch_orders_as_baskets()  # [[p1,p2], [p3], ...]
    model = Recommender()
    model.fit(orders)
    return model
