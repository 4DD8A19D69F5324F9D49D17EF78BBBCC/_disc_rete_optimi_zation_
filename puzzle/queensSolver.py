#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import shuffle,randint
from RDSet import *
import sys

sys.setrecursionlimit(int(1e9))

time = 1000

def solveIt(n):
    # Modify this code to run your puzzle solving algorithm
    global time
    # cnt = 0
    # sol = range(0, n)
    # shuffle(sol)
    # v = violation(sol)
    # while v != 0:
    #     print 'Doing', cnt
    #     cnt += 1
    #     for i in range(0, n):
    #         for j in range(i+1, n):
    #             sol[i], sol[j] = sol[j], sol[i]
    #             nv = violation(sol)
    #             if nv<v:
    #                 print 'updated from', v, 'to', nv
    #                 v = nv
    #             else:
    #                 sol[i], sol[j] = sol[j], sol[i]

    sol = None
    cnt = 1
    while sol is None:
        time = n*10
        print 'searching iter', cnt
        cnt += 1
        sol = tryall([], 0, n)

    # prepare the solution in the specified output format
    # if no solution is found, put 0s
    outputData = str(n) + '\n'
    if sol is None:
        print 'no solution found.'
        outputData += ' '.join(map(str, [0] * n)) + '\n'
    else:
        outputData += ' '.join(map(str, sol)) + '\n'

    return outputData


# this is a depth first search of all assignments
def tryall(assignment, i, n, can=None, dl=None, dr=None):
    if can is None:
        can = RDSet(n)
        dl = [0] * (2*n+1)
        dr = dl[:]

    global time
    if time < 0:
        return
    time -= 1
    # base-case: if the domains list is empty, all values are assigned
    # check if it is a solution, return None if it is not
    if i == n:
        return assignment[:]
    else:
        trylst = [v for v in can if dl[v+n-i-1] == 0 and dr[v+i-1] == 0]
        shuffle(trylst)
        for v in trylst:
            can[v] = 0
            dl[v+n-i-1] += 1
            dr[v+i-1] += 1
            assignment.append(v-1)
            sol = tryall(assignment, i+1, n, can, dl, dr)
            assignment.pop()
            dl[v+n-i-1] -= 1
            dr[v+i-1] -= 1
            can[v] = 1
            if sol is not None:
                return sol



# checks if an assignment is feasible
def violation(sol):
    n = len(sol)
    ret = 0
    dl = [0]*(2*n+1)
    dr = [0]*(2*n+1)
    for i, v in enumerate(sol):
        ret += dl[v+n-i]
        ret += dr[v+i]
        dl[v+n-i] += 1
        dr[v+i] += 1
    return ret



import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1].strip())
        except:
            print sys.argv[1].strip(), 'is not an integer'
        print 'Solving Size:', n
        print(solveIt(n))

    else:
        print(
        'This test requires an instance size.  Please select the size of problem to solve. (i.e. python queensSolver.py 8)')

