# -*- coding: utf-8 -*-
from algorithm import GN
from matplotlib import pyplot as plt
import networkx as nx
import copy

filepath = r'./data/football.gml'

# 获取社区划分
G = nx.read_gml(filepath)
G_copy = copy.deepcopy(G)
gn_com = GN.partition(G_copy)
print(gn_com)

# 可视化
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=False, node_size=70, width=0.5, node_color=gn_com)
plt.show()

V = [node for node in G.nodes()]
com_dict = {node:com for node, com in zip(V, gn_com)}
k = max(com_dict.values()) + 1
com = [[V[i] for i in range(G.number_of_nodes()) if gn_com[i] == j] for j in range(k)]

# 构造可视化所需要的图
G_graph = nx.Graph()
for each in com:
  G_graph.update(nx.subgraph(G, each))  #
color = [com_dict[node] for node in G_graph.nodes()]

# 可视化
pos = nx.spring_layout(G_graph, seed=4, k=0.33)
nx.draw(G, pos, with_labels=False, node_size=1, width=0.1, alpha=0.2)
nx.draw(G_graph, pos, with_labels=True, node_color=color, node_size=70, width=0.5, font_size=5, font_color='#000000')
plt.show()