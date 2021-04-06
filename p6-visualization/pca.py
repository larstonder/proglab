"""Implementation of the Principal Component Analysis"""

import numpy as np
from scipy.sparse.linalg import eigs
from dimred import DimRed


class PCA(DimRed):
    """Subclass of dimred, Implementation of Dimensionality reduction using Principal Component Analysis"""
    dataset = None
    length_of_data = None
    d = 2

    def __init__(self):
        super().__init__()

    def get_description(self):
        return "Implementation of Dimensionality reduction using Principal Component Analysis"

    def reduce_dimensions(self, dataset):
        self.dataset = dataset
        self.length_of_data = len(dataset)
        return self.transform()

    def fit(self):
        """Method for fiting a PCA model for the dataset"""
        centered_data = self.center_data()
        D = len(centered_data[0])
        covarance_matrix_sigma = np.cov(centered_data.T)
        if D - 1 > self.d:
            [eigvals, eigvecs] = eigs(covarance_matrix_sigma, k=self.d)
        elif D - 1 == self.d:
            [eigvals, eigvecs] = np.linalg.eigh(covarance_matrix_sigma)
            index_eigvecs_of_largest_eigvals = np.argsort(eigvals)[::-1]
            eigvecs = eigvecs[:, index_eigvecs_of_largest_eigvals[:self.d]]
        return np.real(eigvecs), centered_data

    def transform(self):
        """Method for transforming the dataset to 2 dimentions"""
        eigvecs, centered_data = self.fit()
        projected_data = centered_data @ eigvecs
        return projected_data


    def center_data(self):
        """Method for centering the data"""
        my = np.mean(self.dataset, axis=0)
        centered_data = self.dataset - my
        print(centered_data.shape)
        return centered_data
