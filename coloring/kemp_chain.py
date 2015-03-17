import random
import numpy as np
from collections import Counter
import networkx as nx
from math import exp


def get_idx_with_color(coloring,c):
    ret = [] 
    for i,col in enumerate(coloring):
        if col == c:
            ret.append(i)
    return ret
def get_swapping_set(G,coloring,c1,c2):
    c1_nodes = set(get_idx_with_color(coloring,c1))
    c2_nodes = set(get_idx_with_color(coloring,c2))  
    cset = set()
    subG = G.subgraph(c1_nodes|c2_nodes)
    comps = nx.connected.number_connected_components(subG)
    if comps!=1:
        subGs = list(nx.connected.connected_component_subgraphs(subG))
        subG = random.choice(subGs)
    
    for x in subG.nodes():
        if len(subG[x])==0:
            cset.add(x)
    return c1_nodes-cset,c2_nodes-cset,cset


def kemp_chains(G,coloring):   
    c1,c2 = random.sample(set(coloring),2)
    s1,s2,ss = get_swapping_set(G,coloring ,c1, c2)
    
    ret = np.copy(coloring)
    for x in s1:
        ret[x] = c2
    for x in s2:
        ret[x] = c1
    return ret
        

def get_objective(coloring):
    return sum(v**2 for v in Counter(coloring).values())



def get_allowed(G,coloring):
    allowed = []
    colorset = set(coloring)
    for c1 in colorset:
        for c2 in colorset:
            if c1<c2:
                s1,s2,ss = get_swapping_set(G, coloring, c1, c2)
                if len(ss)!=0:
                    allowed.append((c1,c2))
    return allowed

def local_optimize(G,coloring,iters = 1000):
    now = coloring[:]
    

    obj = get_objective(now)
    
    
    for i in range(iters):
        current = kemp_chains(G,now)
        obj_current = get_objective(current)
        
        if obj_current+4>=obj:
            now = current.copy()
            obj = max(obj_current,obj)
    return now
