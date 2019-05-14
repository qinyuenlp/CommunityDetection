# -*- coding:utf-8 -*-
'''
Reference

Paper
----------
Luxburg U V. A tutorial on spectral clustering[J]. Statistics and Computing, 2007, 17(4): 395-416

Blog
----------
https://blog.csdn.net/waleking/article/details/7584084

Example
----------
>  filepath = r'.\LoadData.gml'
>  G = nx.read_gml(filepath)
>  k = 9
>  a = partition(G, k)
>  print(a)
'''
import networkx as nx
import numpy as np
from sklearn.cluster import KMeans
import scipy.linalg as linalg

def partition(G, k, normalized=False):
    A = nx.to_numpy_array(G)
    D = degree_matrix(G)
    L = D - A
    Dn = np.power(np.linalg.matrix_power(D, -1), 0.5)
    L = np.dot(np.dot(Dn, L), Dn)
    if normalized:
        pass
    eigvals, eigvecs = linalg.eig(L)
    n = len(eigvals)

    dict_eigvals = dict(zip(eigvals, range(0, n)))
    k_eigvals = np.sort(eigvals)[0:k]
    eigval_indexs = [dict_eigvals[k] for k in k_eigvals]
    k_eigvecs = eigvecs[:, eigval_indexs]
    result = KMeans(n_clusters=k).fit_predict(k_eigvecs)
    return result

def degree_matrix(G):
    n = G.number_of_nodes()
    V = [node for node in G.nodes()]
    D = np.zeros((n, n))
    for i in range(n):
        node = V[i]
        d_node = G.degree(node)
        D[i][i] = d_node
    return np.array(D)

if __name__ == '__main__':
    filepath = r'.\football.gml'
    
    G = nx.read_gml(filepath)
    k = 12
    a = partition(G, k)
