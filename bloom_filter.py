class BloomFilter:
    def __init__(self, k: int, n: int):
        '''Initializes the bloom filter
           Parameters:
            hf - hash function to be applied
            k - number of hash functions to be applied
            n - bloom filter dimension'''
        assert k > 0, "k must be greater than 0"
        assert n > 0, "n must be greater than 0"
        self._k = k
        self._n = n
        self._m = 0
        self._bf = [0 for _ in range(n)]
    
    @property
    def k(self):
        return self._k
    
    @property
    def n(self):
        return self._n

    @property 
    def m(self):
        return self._m
    
    def _hf(self, key):
        return abs(hash(key))
    
    def add(self, element: str):
        '''Adds an element to the Bloom Filter'''
        assert element is not None, "element is not valid"
        for i in range(self._k):
            p = self._hf(str(element)+str(i)) % self._n
            self._bf[p] = 1
        self.m += 1

    def member(self, element: str):
        '''Checks if element is member of bloom filter'''
        assert element is not None, "element is not valid"
        for i in range(self.k):
            p = self._hf(str(element)+str(i)) % self._n
            if self._bf[p] == 0:
                return False
        return True 

    def __repr__(self):
        return f"BloomFilter(k={self._k}; n={self._n}; m={self._m})"