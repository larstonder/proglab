"""Implementation of the Principal Component Analysis"""

import numpy as np
import scipy as sp
from dimred import DimRed


class PCA(DimRed):
    """Subclass of dimred, Implementation of Dimensionality reduction using Principal Component Analysis"""
    dataset = None
    length_of_data = None
    d = 2

    def __init__(self):
        super().__init__(self)

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
        covarance_matrix_sigma = np.cov(centered_data, self.dataset)
        transformation_matrix = np.array()
        #Tror D er dimensjonen på covariance matrisen, og d er ønsket dimensjon
        if D - 1 > self.d:
            eigvals, eigvecs = sp.sparse.linalg.eigs(covarance_matrix_sigma)
        elif D - 1 == self.d:
            eigvals, eigvecs = np.linalg.eigh(covarance_matrix_sigma)
        eignvals_with_eigenvecs = []
        for i in range(len(eigvals)):
            eignvals_with_eigenvecs.append((eigvals[i], eigvecs[i]))
        for i in range(self.d):
            largest_eigenval = 0
            index_of_largest_eigenval = 0
            for j in range(len(eignvals_with_eigenvecs)):
                if eignvals_with_eigenvecs[j][0] > largest_eigenval:
                    largest_eigenval = eignvals_with_eigenvecs[j][0]
                    index_of_largest_eigenval = j
            np.append(transformation_matrix, eignvals_with_eigenvecs[index_of_largest_eigenval][1])
            eignvals_with_eigenvecs.pop(index_of_largest_eigenval)

        return transformation_matrix, centered_data

    def transform(self):
        """Method for transforming the dataset to 2 dimentions"""
        transformation_matrix, centered_data = self.fit()
        projected_data = np.dot(transformation_matrix, centered_data)
        return projected_data #Denne dataen som skal plotes med matplotlib


    def center_data(self):
        """Method for centering the data"""
        my = self.dataset.sum / self.length_of_data
        centered_data = np.array() 
        for datapoint in self.dataset:
            centered_point = np.subtract(datapoint, my)
            np.append(centered_data, centered_point, axis=0)
        return centered_data
