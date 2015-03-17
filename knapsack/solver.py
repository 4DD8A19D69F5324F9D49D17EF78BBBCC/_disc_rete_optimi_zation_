#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import numpy as np
import bisect
import random
import sys
Item = namedtuple("Item", ['index', 'value', 'weight'])


sys.setrecursionlimit(1000000)

def solve_dp(data,capacity):
    dp = [ [0] *(capacity+1) ]
    p = [ [-1] *(capacity+1) ]
    
    for i in xrange(len(data)):
        dp.append(list(dp[i]))
        p.append( [0] * (capacity + 1))
        item = data[i];
        for x in xrange(item.weight, capacity + 1):
            tmp0 = dp[i][x];
            tmp1 = dp[i][x - item.weight] + item.value;
            if tmp1 > tmp0:
                p[i + 1][x] = 1;
                dp[i + 1][x] = tmp1;
            else:
                p[i + 1][x] = 0;
                dp[i + 1][x] = tmp0;
    last = dp[len(dp) - 1]
    _max = 0
    _p = 0
    for i in xrange(len(last)):
        if last[i] > _max:
            _max = last[i]
            _p = i
    _ans = _max
    _step = []
    _cur = len(dp) - 1
    while _cur != 0:
        _step.append(p[_cur][_p])
        _p -= p[_cur][_p] * data[_cur - 1].weight;
        _cur -= 1;
    _step.reverse()
    return _max, _step




def solve_bb(data,capacity):
    data = sorted(data,key = lambda x: (1.0*x.value/x.weight,-x.weight),reverse=True)
    n = len(data)
    
    value_csum = np.cumsum([item.value for item in data])
    weight_csum = np.cumsum([item.weight for item in data])
    
    def get_relaxed_value(start,capacity):
        if start == 0:
            vd = wd = 0
        else:
            vd = value_csum[start-1]
            wd = weight_csum[start-1]
        p = bisect.bisect(weight_csum,capacity+wd)
        lb = value_csum[p-1]-vd if p!=0 else 0
        space = capacity+wd-(weight_csum[p-1] if p!=0 else 0)
        ub = lb  + (1.0*space/data[p].weight * data[p].value if p!=n else 0)
        return lb,ub
  
    class Solution(object):
        def __init__(self):
            self.bestobj = 0
            self.bestsol = [0]*n
            self.iters = 0
        def update(self,solution,obj):
            if obj>self.bestobj:
                self.bestobj = obj
                self.bestsol = list(solution)
            
            
    now = Solution()
    tmp = [0]*n
    
    limit = 10000000
    def dfs(i=0,obj = 0,cap=capacity):
        now.iters +=1
        
        if i==n or capacity==0:
            now.update(tmp, obj)
            return
        else:
            lb,ub = get_relaxed_value(i+1, cap)
            if obj+ub<=now.bestobj or now.iters>limit:
                return
            if data[i].weight<=cap:
                tmp[data[i].index]=1
                dfs(i+1,obj+data[i].value,cap-data[i].weight)
                tmp[data[i].index]=0
            dfs(i+1,obj,cap)
    dfs()
    
    return now.bestobj,now.bestsol







def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    
    
    #print solve_bb(items, capacity)
    value,taken = solve_bb(items, capacity)
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

