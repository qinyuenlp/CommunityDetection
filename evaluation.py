# -*- coding:utf-8 -*-

import community
import math
import numpy as np

def NMI(A, B):
    '''
    A, B should be list or array
    '''
    if len(A) != len(B):
        return ValueError('len(A) should be equal to len(B)')

    A = np.array(A)
    B = np.array(B)
    total = len(A)
    A_ids = set(A)
    B_ids = set(B)
    #Mutual information
    MI = 0
    eps = 1.4e-45
    for idA in A_ids:
        for idB in B_ids:
            idAOccur = np.where(A == idA)
            idBOccur = np.where(B == idB)
            idABOccur = np.intersect1d(idAOccur, idBOccur)
            px = 1.0*len(idAOccur[0])/total
            py = 1.0*len(idBOccur[0])/total
            pxy = 1.0*len(idABOccur)/total
            MI = MI + pxy*math.log(pxy/(px*py) + eps,2)
    # Normalized Mutual information
    Hx = 0
    for idA in A_ids:
        idAOccurCount = 1.0*len(np.where(A == idA)[0])
        Hx = Hx - (idAOccurCount/total)*math.log(idAOccurCount/total + eps, 2)
    Hy = 0
    for idB in B_ids:
        idBOccurCount = 1.0*len(np.where(B == idB)[0])
        Hy = Hy - (idBOccurCount/total) * math.log(idBOccurCount/total + eps, 2)
    MIhat = 2.0*MI/(Hx + Hy)
    return MIhat

def modularity(partition, graph, weight='weight'):
    return community.modularity(partition, graph, weight)

def ARI(partition, real_partition):
    pass

def to_community(distinct, partition):
    """ Turn partition(a list) to list of communities(a list of sets)"""
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
