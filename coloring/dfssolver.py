
import numpy as np
import random

class CDict(object):
    def __init__(self,n,m):
        self.n = n
        self.m = m
        self.adj = np.ones((n,m),dtype=int)
        mkSet = lambda : set(range(m))        
        self.dct = {i:mkSet() for i in range(n)}
        self.sz = [m for i in range(n)]
        self.cliques = []
        self.stats = [0,0]
        
    def delete(self,i,j):
        if self.adj[i,j]:
            self.sz[i]-=1
            self.adj[i,j]=0
            self.dct[i].remove(j)
    
    def add(self,i,j):
        if not self.adj[i,j]:
            self.sz[i]+=1
            self.adj[i,j] = 1
            self.dct[i].add(j)


    def is_okay_with_clique(self,color):
        for clique in self.cliques:
            unionset = set()
            for node in clique:
                if color[node]!=-1:
                    unionset.add(color[node])
                else:
                    unionset |= self.dct[node]
            if len(unionset)<len(clique):
                self.stats[0]+=1
                return False
        self.stats[1]+=1
        return True
                

config_constraint_prop = 0

def solve_coloring_with_limit(G,limit,kill=[False],cliques=[]):
    n = G.number_of_nodes()    
    sol = np.ones(G.number_of_nodes(),dtype=int) 
    sol*=-1    
    allowed =CDict(n,limit)
    status = [None]
    stats = {'SearchNodes':0}
    
    
    for i in range(n):
        for j in range(limit):
            if random.random()<0.1:
                allowed.delete(i,j)
    
    def dfs(i,un=n):
        stats['SearchNodes']+=1
        if kill[0]:
            raise Exception
        if status[0] is not None:
            return
        if un==0:
            status[0]=sol.copy()
            return
        
        
        pruned_list = []
        for color in allowed.dct[i]:
            pruned = []
            assigned = []
            stop = [False]
            
            def prune(node,color):
                sol[node]=color
                assigned.append((node,color))
                if stop[0] or status[0] is not None:
                    return
                for neighbor in G[node]:
                    if sol[neighbor]==-1:
                        if allowed.adj[neighbor,color]:
                            allowed.delete(neighbor,color)
                            pruned.append((neighbor,color))
                        if allowed.sz[neighbor]==0:
                            stop[0] = True
                            return False
                        if config_constraint_prop and allowed.sz[neighbor]==1:
                            prune(neighbor,next(iter(allowed.dct[neighbor])))
                    else:
                        if sol[neighbor]==color:
                            stop[0] = True
                            return False
                return True
            prune(i,color)
            for x,y in pruned:
                allowed.add(x,y)
            for x,c in assigned:
                sol[x]=-1
            if not stop[0]:
                pruned_list.append((pruned,assigned))
            
        pruned_list.sort(key=lambda x: (len(x[1]),random.randint(0,100)))
        
        
        for plist,assigned in pruned_list:
            for x,c in assigned:            
                sol[x]=c
            
            for x,y in plist:
                allowed.delete(x,y)
            if un-len(assigned)==0:
                dfs(-1,0)
            deg = allowed.sz
            nxt = -1
            ops = 10000             
            for k in range(n):
                
                key = deg[k]
                if sol[k]==-1 and key<ops:
                    ops=key
                    nxt = k
            if nxt!=-1:
                dfs(nxt,un-len(assigned))
            for x,y in plist:
                allowed.add(x,y)
            for x,c in assigned:
                sol[x]=-1
    dfs(0)
    
    print stats
    if status[0] is None:
        return None
    return status[0]