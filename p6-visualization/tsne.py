
"""Implementation of t-SNE"""

from dimred import DimRed

class TSNE(DimRed):
    """t-SNE implementation class"""

    def __init__(self):
        DimRed.__init__(self)

    def get_description(self):
        return "Student t-Distributed Stochastic Neighbor Embedding"

    def reduce_dimensions(self, dataset):
        raise NotImplementedError()
