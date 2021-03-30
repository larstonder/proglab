
"""An abstrct class, see DimRed :)"""

class DimRed:
    """Abstract class for Dimensionality reduction algorithms"""

    def __init__(self):
        pass

    def get_description(self):
        """A Description of the dimensionality reduction algorithm"""
        raise NotImplementedError()

    def reduce_dimensions(self, dataset):
        """Reduces the dimensions of the dataset"""
        raise NotImplementedError()
