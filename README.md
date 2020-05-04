# CommunityDetection
[![Python](https://img.shields.io/badge/Python-3.6-blue.svg)](https://www.python.org/)
[![field](https://img.shields.io/badge/networkx-2.4-brightgreen)](https://github.com/networkx/networkx)  
△.这些内容是我研究社区发现时的一些实验代码，主要基于```networkx```。**\*部分代码借鉴了网友的分享，已给出参考来源。**  
△.将这些代码分享出来，一是为了给刚刚进行复杂网络社区发现相关研究的朋友带来一些便利，二是以备日后不时之需。  
△.受限于学术水平与编程能力，若代码有错误或不足之处，欢迎朋友们的指正！  
## 使用示例
以美国大学橄榄球联盟的比赛数据集(football)为例，将该网络划分为12个社区，并可视化  
```
from algorithm import SpectralClustering
from matplotlib import pyplot as plt
import networkx as nx

filepath = r'./data/football.gml'
G = nx.read_gml(filepath)

# 获取社区划分
k = 12
sc_com = algorithm.SpectralClustering.partition(G, k)  # 谱聚类

# 可视化(原图布局)
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=False, node_size=70, width=0.5, node_color=sc_com)
plt.show()
```
可得到原图布局的可视化结果，如下图所示  
![SpectralClustering_ori](https://github.com/QinY-Stat/CommunityDetection/blob/master/images/spectral%20clustering_ori.png)  
上图所展示的是在**原Graph的拓扑结构下**，利用颜色对不同社区的节点加以区分。但如果想达到**同社区节点联系紧密，不同社区节点联系稀疏**的效果，则在获取社区划分(以谱聚类结果sc_com为例)后，还需要进行以下操作:  
```
# 获取每个社区所包含的节点
V = [node for node in G.nodes()]
com_dict = {node:com for node, com in zip(V, sc_com)}
com = [[V[i] for i in range(G.number_of_nodes()) if sc_com[i] == j] for j in range(k)]

# 构造可视化所需要的图
G_graph = nx.Graph()
for each in com:
  G_graph.update(nx.subgraph(G, each))
color = [com_dict[node] for node in G_graph.nodes()]

# 可视化(社区布局)
pos = nx.spring_layout(G_graph, seed=4, k=0.33)
nx.draw(G, pos, with_labels=False, node_size=1, width=0.1, alpha=0.2)
nx.draw(G_graph, pos, with_labels=True, node_color=color, node_size=70, width=0.5, font_size=5, font_color='#000000')
plt.show()
```
结果得到下图  
![SpectralClustering](https://github.com/QinY-Stat/CommunityDetection/blob/master/images/spectral%20clustering.png)  

**需要注意的是**，对于**GN**这类图划分算法，原图$G$在经过社区发现之后其结构已经被破坏，要对此类算法的结果进行可视化，需要先保存原图结构，如下所示
```
from algorithm import GN
from matplotlib import pyplot as plt
import networkx as nx
import copy

filepath = r'./data/football.gml'
G = nx.read_gml(filepath)
G_copy = copy.deepcopy(G)  # 复制一个图来进行社区发现

# 获取社区划分
gn_com = GN.partition(G_copy)

# 可视化(原图布局)
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

# 可视化(社区布局)
pos = nx.spring_layout(G_graph, seed=4, k=0.33)
nx.draw(G, pos, with_labels=False, node_size=1, width=0.1, alpha=0.2)
nx.draw(G_graph, pos, with_labels=True, node_color=color, node_size=70, width=0.5, font_size=5, font_color='#000000')
plt.show()
```

## 内容
### 社区发现算法
算法名称 | 参考文献 | 代码参考链接 | 相关说明
---- | ---- | ---- | ----
GN(Girvan&Newman) | [《Community structure in social and biological networks》](https://arxiv.org/abs/cond-mat/0112110) | [zzz24512653](https://github.com/zzz24512653/CommunityDetection/blob/master/algorithm/GN.py) | -
Spectral Clustering | [《A tutorial on spectral clustering》](https://arxiv.org/abs/0711.0189) | [waleking](https://blog.csdn.net/waleking/article/details/7584084) | [推导](https://github.com/TUFE-I307/Seminar-MachineLearning/tree/master/谱聚类)


### 社区发现评价指标
#### 1. 模块度(Modularity)
![modularity](https://github.com/QinY-Stat/CommunityDetection/blob/master/images/modularity.png)  
相关博客: [模块度发展历程](https://qinystat.gitee.io/2020/01/22/Modularity/)
#### 2. 标准化互信息(Normalized Mutual Information(NMI))
NMI代码参考链接：[bethansy](http://www.cnblogs.com/bethansy/p/6890972.html)
![NMI](https://github.com/QinY-Stat/CommunityDetection/blob/master/images/NMI.png)  
      
