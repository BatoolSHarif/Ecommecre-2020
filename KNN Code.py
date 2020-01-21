import pandas as pd
from sklearn.neighbors import NearestNeighbors

def get_nei():
    df = pd.read_csv('product_tags.csv', names= ['id','product_id','tag_id'])
    df.set_index('product_id')
    dummies = pd.get_dummies(df['tag_id'])
    concat = pd.concat([df,dummies], axis=1)
    merged = concat.groupby(by=['product_id'],as_index=False).sum()
    merged.set_index('product_id')
    print(merged)
    headers = list(set(df['tag_id'].tolist()))
    print(headers)
    X = merged[headers]
    nbr = NearestNeighbors(n_neighbors=4, algorithm='ball_tree').fit(X)
    distances, indices = nbr.kneighbors(X)
    products = list(set(df['product_id'].tolist()))
    result = {}
    indices = indices.tolist()
    prod_to_index = {}
    for index, prod_id in enumerate(products):
        product_index = merged[merged['product_id']==prod_id].index.values[0]
        prod_to_index[product_index] = prod_id
    print(prod_to_index)
    return indices, prod_to_index

def prod_index(indices, prod_to_index):
    results = {}
    for index in indices:
        res = index[1:]
        header = prod_to_index[index[0]]
        item = []
        for i in res:
            item.append(prod_to_index[i])
        results[header] = item
    return results