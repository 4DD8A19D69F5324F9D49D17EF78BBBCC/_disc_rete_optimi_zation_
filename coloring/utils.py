import numpy as np
from multiprocessing import Process, Queue


def greedy_coloring(G):
    n = G.number_of_nodes()
    deg = G.degree()
    order = sorted(deg.keys(),key = lambda x: (-deg[x],0))
    color = np.zeros(G.number_of_nodes(),dtype=int)-1    
    for node in order:
        colorset = set(color[neighbor] for neighbor in G[node])        
        for i in range(n):
            if i not in colorset:
                color[node]=i
                break
    return color

def run_in_sub(f,*args,**kwargs):
    queue = Queue()
    def wrapper(q,*args,**kwargs):
        
        q.put(f(*args[0],**kwargs))
    p = Process(target=wrapper, args=tuple([queue]+list(args)),kwargs=kwargs)
    p.start()
    p.join() # this blocks until the process terminates
    result = queue.get()
    return result