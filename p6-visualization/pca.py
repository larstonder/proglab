"""Implementation of the Principal Component Analysis"""

import numpy as np
import scipy as sp


class PCA:
    """Implementation of the Principal Component Analysis"""
    dataset = None
    length_of_data = None

    def __init__(self, dataset):
        self.dataset = dataset
        self.length_of_data = len(dataset)

    def fit(self):
        centered_data = self.center_data()
        covarance_matrix_sigma = np.cov(centered_data, self.dataset)
        transformation_matrix = np.array()
        #TODO Finne ut hva D og d er, filtrere å legge til de riktige eigenvektorene i transformasjons matrisen
        if D - 1 > d:
            eigvals, eigvecs = sp.sparse.linalg.eigs(covarance_matrix_sigma)
        elif D - 1 == d:
            eigvals, eigvecs = np.linalg.eigh(covarance_matrix_sigma)

        return transformation_matrix, centered_data

    def trasform(self):
        transformation_matrix, centered_data = self.fit()
        projected_data = np.dot(transformation_matrix, centered_data)
        return projected_data #Denne dataen som skal plotes med matplotlib


    def center_data(self):
        my = self.dataset.sum / self.length_of_data
        centered_data = np.array()
        for datapoint in self.dataset:
            centered_point = np.subtract(datapoint, my)
            np.append(centered_data, centered_point, axis=0)
        return centered_data
