#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import itertools
from collections import Counter

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    nodeCount = int(firstLine[0])
    edgeCount = int(firstLine[1])

    edges = []
    degree = []
    for i in range(0, nodeCount):
        edges.append([])
        degree.append(0)
    
    for i in range(1, edgeCount + 1):
        line = lines[i]
        parts = line.split()      
        edges[int(parts[0])].append(int(parts[1]));
        edges[int(parts[1])].append(int(parts[0]));
        degree[int(parts[0])] += 1
        degree[int(parts[0])] += 1

    def greedy_coloring(ordering, now):
        count = 0
        color = [-1] * nodeCount
        
        for item in ordering:
            vis = [0] * (count + 1)
            for x in edges[item]:
                if color[x] != -1:
                    vis[color[x]] = 1
            for i in range(0, count):
                if vis[i] == 0:
                    color[item] = i;
                    break;
            if color[item] == -1:
                color[item] = count;
                count += 1;
        value = 0;
        
        c = Counter(color);
        
        for item in c:
            value+= c[item]**2
        value -= len(c)**2
        return (count, color, value)
        
        
        
        
    print 'node#', nodeCount, 'edge#', edgeCount    
    # build a trivial solution
    # every node has its own color
    solution = greedy_coloring(range(0, nodeCount), 10000)
    

    order = map(lambda x:x[1], sorted(zip(degree, range(0, nodeCount))))
    random.shuffle(order)
    _notupdated = 0
    _canceled = 0
    _prev = -2147483648
    _max = -2147483648
    for i in range(0, 1000):
        if i % 100 == 0:
            print 'iter', i
        r1 = random.randint(0, nodeCount - 1)
        r2 = random.randint(0, nodeCount - 1)
        if r1 == r2:
            continue
        t = order[r1]
        order[r1] = order[r2]
        order[r2] = t
        sol = greedy_coloring(order, solution[0])
        if sol[0] < solution[0]:
            print 'updated from ', solution[0], 'to ', sol[0]
            solution = sol
        if sol[2] >= _prev:
            _prev=sol[2]
            if sol[2]>_max:
                _max=sol[2]
                print _max
        else:
            t = order[r1]
            order[r1] = order[r2]
            order[r2] = t
            _notupdated += 1

            

    # prepare the solution in the specified output format
    outputData = str(solution[0]) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, solution[1]))

    return outputData


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

