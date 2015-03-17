


from gurobipy import *
from networkx import nx
from parsing import *
import random
from collections import defaultdict


def all_large_cliques_upto(G,limit=1000):
    GG = G.copy()
    cliq_iter = nx.find_cliques(GG)
    
    for i in range(limit):
        try:
            cliq = []
            while len(cliq)<3:
                cliq = next(cliq_iter)
                
        except StopIteration:
            break
        
        yield cliq
        



def find_all_clqs(G):
    u = set()

    for item in all_large_cliques_upto(G, 1000000):
        u.add(tuple(item))

    print len(u)
            
    for x,y in G.edges():
        u.add((x,y))
    
    return u





def set_cover_model(G,clqs):
    n = G.number_of_nodes()
    m = len(clqs)
    model = Model()
    
    decision_vars = [model.addVar(vtype=GRB.BINARY) for i in range(m)]
    
    model.update()
    ridx = [[] for i in range(n)]
    
    for i,clq in enumerate(clqs):
        for elem in clq:
            ridx[elem].append(i)
    
    
    for lst in ridx:
        varlst = map(lambda x:decision_vars[x], lst)
        constraint = quicksum(varlst) >= 1
        model.addConstr(constraint)
    model.update()


    model.setObjective(quicksum(decision_vars),GRB.MINIMIZE)
    model.setParam('TimeLimit',60)
    model.optimize()
    xs = [v.x for v in model.getVars()]    
    
    
    
    c = [-1]*n
    no = 0
    for x,clq in zip(xs,clqs):
        if x == 1:
            for elem in clq:
                c[elem]=no
            no+=1
    return c




def convert_to_cliques(coloring):
    ridx = defaultdict(list)
    for i,item in enumerate(coloring):
        ridx[item].append(i)
    return set([ frozenset(x) for x in ridx.values()])


            
    
    
    

def cliquesolve(G):
    C = nx.complement(G)
    u= find_all_clqs(C)
    solution = set_cover_model(G, u)
    return solution

if __name__ == '__main__':
    G = parse_input(get_input('./data/gc_250_9'))
    C = nx.complement(G)
    u= find_all_clqs(C)
    result = set_cover_model(G, u)
    print result
#     ans = graph_coloring_problem_or(G,35)
#     print ans,len(set(ans))   
