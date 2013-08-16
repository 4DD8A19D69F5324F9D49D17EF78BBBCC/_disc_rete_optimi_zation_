#
# A fast set that support deletion resume and iteration
#

from random import randint
class RDSet(object):

    def __init__(self, n):
        self.prev = range(-1, n)
        self.next = range(1, n + 2)
        self.prev[0] = n
        self.next[n] = 0
        self.size = n
        self.vis = [1] * (n+1)
        self.length = n

    def __iter__(self):
        return RDSetIter(self)

    def __len__(self):
        return self.length

    def __getitem__(self, item):
        return self.vis[item]

    def __setitem__(self, key, value):
        if value == 0:
            self.remove(key)
        else:
            self.resume(key)

    def remove(self, x):
        assert(0 < x <= self.size)
        if self.vis[x] == 1:
            self.vis[x] = 0
            self.prev[self.next[x]] = self.prev[x]
            self.next[self.prev[x]] = self.next[x]
            self.length -= 1

    def resume(self, x):
        assert(0 < x <= self.size)
        if self.vis[x] == 0:
            self.vis[x] = 1
            self.next[self.prev[x]] = x
            self.prev[self.next[x]] = x
            self.length += 1

    def getprev(self, x):
        return self.prev[x]

    def getnext(self, x):
        return self.next[x]



class RDSetIter(object):
    def __init__(self, rdset):
        self.rdset = rdset
        self.current = 0

    def __iter__(self):
        return self

    def next(self):
        x = self.rdset.getnext(self.current)
        if x == 0:
            raise StopIteration
        else:
            self.current = x
            return x


