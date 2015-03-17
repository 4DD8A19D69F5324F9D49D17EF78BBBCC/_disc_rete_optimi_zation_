#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np
import sys
import random
from Numberjack import *
from parsing import *
from utils import *
from kemp_chain import *
from cliquesolve import convert_to_cliques, set_cover_model
from time import sleep

sys.setrecursionlimit(100000)





def graph_coloring_with_fixed(cliqs,G,limit,fixed=[]):
    n = G.number_of_nodes()
    model = Model()
    
    if fixed==[]:
        fixed = [-1]*n
    
    
    fixed = [int(x) for x in fixed]    
    
    xs = [ Variable(limit) for i in range(n)]
    ncons =0
    
    for cliq in cliqs:
        model.add(AllDiff([xs[i] for i in cliq]))
        ncons +=1    
    for i in range(len(fixed)):
        if fixed[i]!=-1:
            model.add(xs[i]==int(fixed[i]))
    for x,y in G.edges_iter():
        if fixed[x]!=-1 and fixed[y]!=-1:
            continue 
        
        if fixed[x]!=-1:
            model.add(fixed[x] != xs[y])
        elif fixed[y]!=-1:
            model.add(xs[x] !=fixed[y])
        else:
            model.add(xs[x] != xs[y])
            ncons +=1    
    
    #model.add(Minimize(Max(xs)))
    print '#Constraints=',ncons
    return xs,model




def perturb(G,ans,d,p):
    s = set(ans)
    delset = set(random.sample(s,min(d,len(s))))
    s-=delset
    if -1 in s:
        s.remove(-1)
    dct = {}
    for i,elem in enumerate(s):
        dct[elem] = i
    ret= [dct[ans[i]] if ans[i]  in dct and random.random()<p else -1 for i in range(len(ans))]
    
    
    r = random.randint(0,G.number_of_nodes()-1)
    for x in G[r]:
        if random.random()>p:
            ret[x] = -1
    
    
    return ret


    
def solve_with_numberjack2(var,model):   
    solver = model.load('Mistral2',X=var)
    solver.setNodeLimit(10000)
    solver.setVerbosity(2)
#     solver.setHeuristic('MinDomain','Lex',1)
    if solver.solve():
        ret= [ int(str(x)) for x in var]
        return ret


def solve(G,save=None):
    if save:
        solution = save
    else:
        solution = greedy_coloring(G)
    
    n = G.number_of_nodes()
    m = G.number_of_edges()
    C = n*(n-1)/2
    ratio = m*1.0/C
    
    
    
    
    
    
    def localsolve():
        tmpsolution = np.array(solution)
        failed = 0
        nc = len(set(solution)) -1
        
        p = 0.25
        
        restart_flag = False
        while True:
            try:
                print 'trying:',nc
                oldobj = get_objective(tmpsolution)
                tmpsolution = local_optimize(G, tmpsolution, 5000)
                newobj =  get_objective(tmpsolution)
                print oldobj,newobj
                pt = perturb(G, tmpsolution, 7, 0.6+p)
                nblank = sum(x==-1 for x in pt)
            
                print '#blank=',nblank
                var,model = graph_coloring_with_fixed([],G,nc,pt)
                result = run_in_sub(solve_with_numberjack2,(var,model))
                
                
                
                
                if result is not None:
                    p=0.3
                    result = np.array(result)
                    failed = 0
                    tmpsolution = result
                    print result
                    nc = len(set(result))-1
                else:
                    failed+=1
                    p*=0.999
                    print nc,failed
                if failed>=1000:
                    break
            except KeyboardInterrupt:
                break
        return tmpsolution
    
    
    if ratio>0.8 and n<=300:
        import cliquesolve   
        solution = cliquesolve.cliquesolve(G)
    else:
        solution = localsolve()

    return solution







def solve_it(input_data,save=None):
    # Modify this code to run your optimization algorithm

    # parse the input
    G = parse_input(input_data)
    print G.number_of_nodes(),G.number_of_edges()


    solution = solve(G,save)

    # prepare the solution in the specified output format
    output_data = str(len(set(solution))) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        file_location = sys.argv[1].strip()
        try:
            save = open(file_location+".out").readlines()
            save = [int(x) for x in save[1].split()]
        except:
            save = None
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        G = parse_input(input_data)
        sol= solve_it(input_data,save)
        print sol
        open(file_location+".out","w").write(sol)        
        
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'
