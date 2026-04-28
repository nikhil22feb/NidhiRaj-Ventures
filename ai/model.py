
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def recommend(product_vectors, target_index):
    sims = cosine_similarity([product_vectors[target_index]], product_vectors)[0]
    return np.argsort(sims)[-5:]
