
"""Implementation of t-SNE"""

from dimred import DimRed
from kNN import symmetric_binary_k_nearest

class TSNE(DimRed):
    """t-SNE implementation class"""

    def __init__(self):
        DimRed.__init__(self)
        self.k = 30
        self.max_iterations = 100

    def get_description(self):
        return "Student t-Distributed Stochastic Neighbor Embedding"

    def reduce_dimensions(self, dataset):
        n = len(dataset)

        kNN = symmetric_binary_k_nearest(dataset, self.k)

        Y = np.random.normal(loc=0, scale=10**-4, size=(n, 2))
        g = np.full(shape=n, 1)
        delta = np.full(shape=n, 0)

        for i in range(self.max_iterations):
