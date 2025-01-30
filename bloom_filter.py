import numpy as np

class BloomFilter:
    def __init__(self, k, n):
        '''Initializes the bloom filter
           Parameters:
            hf - hash function to be applied
            k - number of hash functions to be applied
            n - bloom filter dimension'''
        assert k > 0, "k must be greater than 0"
        assert n > 0, "n must be greater than 0"
        self.k = k
        self.n = n
        self.m = 0
        self.bf = np.zeros(n, dtype=bool)
    
    
    def getK(self):
        return self.k
    
    def getN(self):
        return self.n
    
    def getM(self):
        return self.m
    
    def _hf(self, key):
        return np.abs(hash(key))
    
    def add(self, element):
        '''Adds an element to the Bloom Filter'''
        assert element is not None, "element is not valid"
        for i in range(self.k):
            p = self._hf(str(element)+str(i)) % self.n
            self.bf[p] = 1
        self.m += 1

    def member(self, element):
        '''Checks if element is member of bloom filter'''
        assert element is not None, "element is not valid"
        for i in range(self.k):
            p = self._hf(str(element)+str(i)) % self.n
            if self.bf[p] == 0:
                return False
        return True 

    def __repr__(self):
        return f"BloomFilter(k={self.k}; n={self.n}; m={self.m})"