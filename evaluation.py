# -*- coding:utf-8 -*-

import math
import numpy as np
import networkx as nx

def NMI(com, real_com):
    """
    Compute the Normalized Mutual Information(NMI)

    Parameters
    --------
    com, real_com : list or numpy.array
        number of community of nodes
    """
    if len(com) != len(real_com):
        return ValueError('len(A) should be equal to len(B)')

    com = np.array(com)
    real_com = np.array(real_com)
    total = len(com)
    com_ids = set(com)
    real_com_ids = set(real_com)
    #Mutual information
    MI = 0
    eps = 1.4e-45
    for id_com in com_ids:
        for id_real in real_com_ids:
            idAOccur = np.where(com == id_com)
            idBOccur = np.where(real_com == id_real)
            idABOccur = np.intersect1d(idAOccur, idBOccur)
            px = 1.0*len(idAOccur[0])/total
            py = 1.0*len(idBOccur[0])/total
            pxy = 1.0*len(idABOccur)/total
            MI = MI + pxy*math.log(pxy/(px*py) + eps,2)
    # Normalized Mutual information
    Hx = 0
    for idA in com_ids:
        idAOccurCount = 1.0*len(np.where(com == idA)[0])
        Hx = Hx - (idAOccurCount/total)*math.log(idAOccurCount/total + eps, 2)
    Hy = 0
    for idB in real_com_ids:
        idBOccurCount = 1.0*len(np.where(real_com == idB)[0])
        Hy = Hy - (idBOccurCount/total) * math.log(idBOccurCount/total + eps, 2)
    MIhat = 2.0*MI/(Hx + Hy)
    return MIhat

def modularity(G, community):
    """
    Compute modularity of communities of network

    Parameters
    --------
    G : networkx.Graph
        an undirected graph
    community : dict
        the communities result of community detection algorithms
    """
    V = [node for node in G.nodes()]
    m = G.size(weight='weight')  # if weighted
    n = G.number_of_nodes()
    A = nx.to_numpy_array(G)
    Q = 0
    for i in range(n):
        node_i = V[i]
        com_i = community[node_i]
        degree_i = G.degree(node_i)
        for j in range(n):
            node_j = V[j]
            com_j = community[node_j]
            if com_i != com_j:
                continue
            degree_j = G.degree(node_j)
            Q += A[i][j] - degree_i * degree_j/(2 * m)
    return Q/(2 * m)

def ARI(partition, real_partition):
    """ Compute the Adjusted Rand Index"""
    n = len(partition)
    distinct = set(partition)
    real_distinct = set(real_partition)
    communities = to_community(distinct, partition)
    real_communities = to_community(real_distinct, real_partition)

    union = list()
    intersection = list()
    for real_community in real_communities:
        for community in communities:
            intersection += real_community & community
            union += real_community | community
    union = list(set(union))
    for node in intersection:
        union.remove(node)
    a11 = len(intersection)
    num_in_real = len([node for node in union if node in real_communities])
    num_not_in_real = len(union) - num_in_real
    a10 = num_in_real
    a01 = num_not_in_real
    a00 = (n**2 - n)/2 - (a11 + a10 + a01)

    numerator = (a11 + a01) * (a11 + a10) / a00
    denominator1 = (2 * a11 + a01 + a10) / 2
    denominator2 = (a11 + a01) * (a11 + a10) / a00

    test = numerator / (denominator1 + denominator2)
    return a11 - numerator / (denominator1 + denominator2)


def to_community(distinct, partition):
    """
    Turn partition(a list) to list of communities(a list of sets)

    """
    distinct = list(distinct)
    partition = list(partition)
    communities = []
    for com in range(len(distinct)):
        community = []
        for node_index in range(len(partition)):
            if partition[node_index] == distinct[com]:
                community.append(node_index)
        communities.append(set(community))
    return communities