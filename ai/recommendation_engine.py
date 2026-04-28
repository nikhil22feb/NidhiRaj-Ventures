
def recommend(user_history, products):
    scores={}
    for p in user_history:
        scores[p]=scores.get(p,0)+1
    sorted_items=sorted(scores,key=scores.get,reverse=True)
    return sorted_items[:5]
