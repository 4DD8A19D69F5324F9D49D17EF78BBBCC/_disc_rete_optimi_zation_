#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import shuffle,randint,random
from math import exp
import sys
sys.setrecursionlimit(100000000)
def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    parts = lines[0].split()
    warehouseCount = int(parts[0])
    customerCount = int(parts[1])
    
    print 'n=',warehouseCount,'m=',customerCount
    warehouses = []
    for i in range(1, warehouseCount+1):
        line = lines[i]
        parts = line.split()
        warehouses.append((int(parts[0]), float(parts[1])))

    customerSizes = []
    customerCosts = []


    lineIndex = warehouseCount+1
    for i in range(0, customerCount):
        customerSize = int(lines[lineIndex+2*i])
        customerCost = map(float, lines[lineIndex+2*i+1].split())
        customerSizes.append(customerSize)
        customerCosts.append(customerCost)
    global tmpsol
    global remaining
    tmpsol=[0]*customerCount
    remaining = [w[0] for w in warehouses]



#trivival solver
    def solve(order):
        solution = [-1] * customerCount
        capacityRemaining = [w[0] for w in warehouses]
        warehouseIndex = 0

        myord = range(0, customerCount)
        shuffle(myord)
        for c in myord:
            if capacityRemaining[order[warehouseIndex]] >= customerSizes[c]:
                solution[c] = order[warehouseIndex]
                capacityRemaining[order[warehouseIndex]] -= customerSizes[c]
            else:
                warehouseIndex += 1
                assert capacityRemaining[order[warehouseIndex]] >= customerSizes[c]
                solution[c] = order[warehouseIndex]
                capacityRemaining[order[warehouseIndex]] -= customerSizes[c]

        used = [0]*warehouseCount
        for wa in solution:
            used[wa] = 1

        # calculate the cost of the solution
        obj = sum([warehouses[x][1]*used[x] for x in range(0,warehouseCount)])
        for c in range(0, customerCount):
            obj += customerCosts[c][solution[c]]
        return (obj,solution)


    def solve2(lst,curcost,numops):
        initialCost = sum([ warehouses[x][1] for x in lst ] )
        Cost = initialCost
        solution = [-1] * customerCount
        
        if initialCost>=curcost:
            return (1e10,[],-1)
        
        myord = range(0,customerCount)
        shuffle(myord)
        
        lowcost = 1e9
        finalsol = []
        
        for iter in range(numops):
            def r():
                return randint(0,customerCount-1)
            def swp(a,l,r):
                t=a[l]
                a[l]=a[r]
                a[r]=t
            tcost = 0
            feasible = True
            capacityRemaining = [w[0] for w in warehouses]

            r1 = r()
            r2 = r()
            swp(myord,r1,r2)
            for c in myord:
                selected = 0
                tmpcost = 1e8
                for idx in lst:
                    if capacityRemaining[idx] >= customerSizes[c] and customerCosts[c][idx]<=tmpcost:
                        tmpcost=customerCosts[c][idx]
                        selected=idx
                if tmpcost==1e8:
                    feasible=False
                if not feasible:
                    break;
                tcost+=tmpcost
                capacityRemaining[selected]-=customerSizes[c]
                solution[c]=selected
            if feasible and tcost<lowcost:
                lowcost=tcost
                finalsol=solution
            else:
                swp(myord,r1,r2)
        return (Cost+lowcost,finalsol,feasible)

    

    order = range(0,warehouseCount)
    obj,sol=solve(order)


    def randv(n):
        arr = [1] *n + [0] * (warehouseCount-n)
        shuffle(arr)
        return [ i for i,x in enumerate(arr) if x==1]
    

    
    def mutate(v,add,remove):
        if len(v)==1 or len(v)==warehouseCount:
            return v
        vis = [ 0 ] * warehouseCount
        for x in v:
           vis[x]=1
        nl = [ i for i in range(len(vis)) if vis[i]==0]
	shuffle(nl)
        return nl[:add] + v[remove:]
    def cross(v1,v2):
        ll = (len(v1)+len(v2)) //2
        if ll==0:
            ll=1
        vis = [ 0 ] * warehouseCount
        for x in v1+v2:
            vis[x]=1
        nl = [ i for i in range(len(vis)) if vis[i]==1]
        shuffle(nl)
        return nl[:ll]

    solvec= []
    for t in range(1):
        print t
        bvec = [ randv(i%warehouseCount)  for i in range(1,int(warehouseCount))]
        vec = [  ]
	for v in bvec:
		tmp = solve2(v,obj,1)
		if tmp[2]==1:
			vec.append(tmp)
        #vec = [ (1e9,v,0) for v in vec ]
        lvec = len(vec)
        maxsize=500
        for i in range(100):
            if i%20==0:
                print i
            vl = [ mutate(v[1],randint(0,1),randint(0,1)) for v in vec]
            lenvl = len(vl)
            for i,v in enumerate(vl):
                tobj,tsol,can = solve2(v,obj,1)
                if can and tobj<vec[i][0]:
                    vec.append((tobj,v,1))
                    if tobj<obj:
                        print 'updated 2 from',obj,'to',tobj
                        obj=tobj
                        sol=tsol
                        solvec=v
            for i in range(lenvl):
                r1 = randint(0,lenvl-1)
                r2 = randint(0,lenvl-1)
                v = cross(vec[r1][1],vec[r2][1])
                tobj,tsol,can = solve2(v,obj,1)
                if can and tobj<vec[i][0]:
                    vec.append((tobj,v,1))
                    if tobj<obj:
                        print 'updated 3 from',obj,'to',tobj
                        obj=tobj
                        sol=tsol
                        solvec=v
            vec.sort()
            vec = vec[:maxsize]
                
    
    # prepare the solution in the specified output format
    outputData = str(obj) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, sol))

    return outputData


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        print fileLocation
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print 'Solving:', fileLocation
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/wl_16_1)'

