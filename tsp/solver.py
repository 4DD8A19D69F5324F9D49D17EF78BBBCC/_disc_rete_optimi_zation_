#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from random import randint,random,shuffle


def length(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append((float(parts[0]), float(parts[1]),i-1))

    shuffle(points)


    dist = []
    dist_s = []
    # preprocessing distance
    for p1 in points:
        dist.append([])
        for p2 in points:
            dist[-1].append(length(p1,p2))
    for lst in dist:
        dist_s.append([])
        for idx,item in enumerate(lst):
            if item!=0:
                dist_s[-1].append((item,idx))
    for i in range(0,len(dist_s)):
        dist_s[i].sort()
            


    # build a trivial solution
    # visit the nodes in the order they appear in the file
    solution = range(0, nodeCount)

    # calculate the length of the tour
    def calc(solution):
        obj = dist[solution[-1]][solution[0]]
        for index in range(0, len(solution)-1):
            obj += dist[solution[index]][solution[index+1]]
        return obj

    def greedy():
        ret = [0]
        vis = [0]*nodeCount
        vis[0]=1
        
        for i in range(0,nodeCount-1):
            cur = ret[-1]
            tmp = 0
            tdis = 1e10
            for j in range(0,nodeCount):
                if not vis[j]:
                    if dist[j][cur]<tdis:
                        tdis=dist[j][cur]
                        tmp=j
            vis[tmp]=1
            ret.append(tmp)
        return ret


    def incr(o):
        ret = [o[0],o[1]]
        obj = 2*dist[o[0]][o[1]]
        for i in range(2,nodeCount):
            cost = 1e10
            pos = 0
            l = len(ret)
            for j in range(0,l):
                if j+1<l:
                    tcost = dist[ret[j]][o[i]] + dist[o[i]][ret[j+1]] - dist[ret[j]][ret[j+1]]
                else:
                    tcost = dist[ret[j]][o[i]] + dist[ret[0]][o[i]] - dist[ret[0]][ret[-1]]
                if tcost<cost:
                    cost=tcost
                    pos=j
            obj+=cost
            ret.insert(pos+1,o[i])
        return (obj,ret)
    order = range(0,nodeCount)
    shuffle(order)
    obj,solution=incr(order)


    sol=list(solution)


    for i in range(1000):
        if i%10==0:
            print i
        r1 = randint(0,nodeCount-1)
        r2 = randint(0,nodeCount-1)
        if r1==r2:
            continue
        if r1>r2:
            t=r1
            r1=r2
            r2=t
        t = order[r1]
        order[r1]=order[r2]
        order[r2]=t
   
        tobj,tsol=incr(order)
        if obj-tobj>0.1:
            print 'updated from ',obj,'to ',tobj
            obj=tobj
            solution=tsol
        else:
            t = order[r1]
            order[r1] = order[r2]
            order[r2] = t

        def randcmp(a,b):
            return randint(-1,1)
        order_ = order[:r1]+list(sorted(order[r1:r2],randcmp))+order[r2:]
        tobj,tsol=incr(order_)
        if obj-tobj>0.1:
            print 'updated from ',obj,'to ',tobj,'by reverse'
            obj=tobj
            solution=tsol
            order=order_
        

        
        

    
    def ridx(x):
        return points[x][2]
        
    # prepare the solution in the specified output format
    outputData = str(obj) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, map(ridx,solution) ))

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
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)'

