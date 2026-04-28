
def recommend_from_behavior(user_history, all_products):
    # simple frequency-based recommendation
    freq={}
    for p in user_history:
        freq[p]=freq.get(p,0)+1
    sorted_items=sorted(freq,key=freq.get,reverse=True)
    return sorted_items[:5]
