# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 15:12:13 2015

@author: meow
"""

from ortools.constraint_solver import pywrapcp
from networkx import nx


def graph_coloring_problem_or(G,limit,fixed):
    n = G.number_of_nodes()    
    solver = pywrapcp.Solver("Graph coloring")
    xs = [solver.IntVar(0,limit-1) for i in range(n)]
    
    
    
    for u,v in G.edges():
        if fixed[u]!=-1 and fixed[v]!=-1:
            continue
        if fixed[u]!=-1:
            solver.Add(xs[v]!=fixed[u])
        elif fixed[v]!=-1:
            solver.Add(xs[u]!=fixed[v])
        else:
            solver.Add(xs[u]!=xs[v])

    
    for i,x in enumerate(fixed):
        if x!=-1:        
            solver.Add(xs[i]==x)
        
    db= solver.Phase(xs,solver.CHOOSE_MIN_SIZE_LOWEST_MIN,solver.ASSIGN_MIN_VALUE)
    solution = solver.Assignment()
    solution.Add(xs)
    collector = solver.BestValueSolutionCollector(solution)
    limit = solver.FailuresLimit(100000)
    


    obj = solver.Minimize(solver.Max(xs),1)
    
    solver.Solve(db,[collector,limit,obj])
    
    
    if collector.SolutionCount()!=0:
        ans = [int(collector.Value(0,xs[i])) for i in range(n)]
        return ans
    
    return None
    
def get_input(file_location):
    input_data_file = open(file_location, 'r')
    input_data = ''.join(input_data_file.readlines())
    input_data_file.close()
    return input_data
    
def parse_input(input_data):
    G = nx.Graph()
    lines = input_data.split('\n')
    first_line = lines[0].split()
    edge_count = int(first_line[1])
    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
    G.add_edges_from(edges)
    return G


if __name__ == '__main__':
    G = parse_input(get_input('./data/gc_70_9'))
    ans = graph_coloring_problem_or(G,35)
    print ans,len(set(ans))