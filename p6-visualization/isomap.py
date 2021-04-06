"""
Nonlinear reduction algoritm which computes the datasets geodesics and
        performs multidimensional scaling to reduce dimensons
"""
import numpy as np
import sklearn.utils.graph_shortest_path as sg
from dimred import DimRed
from kNN import k_nearest
from scipy.sparse.linalg import eigs


class IsoMap(DimRed):
    """
    Subclass of dimred, Implementation of Dimensionality reduction using ISOMAPING
    """
    k = 20
    m = 2

    def get_description(self):
        return """Nonlinear reduction algoritm which computes the datasets geodesics and 
        performs multidimensional scaling to reduce dimensons"""

    def reduce_dimensions(self, dataset):
        geodesics = self.__compute_geodesics(dataset)
        result = self.__mds(geodesics)
        return result

    def __compute_geodesics(self, dataset):
        """
        Takes high-dimensional data and a user specified parameter
        k as input, and returns a distance
        matrix D, where D_ij is the shortestF-path
        distance between x_i and x_j along the manifold
        """
        distance_matrix = k_nearest(dataset, self.k)
        return sg.graph_shortest_path(distance_matrix)
    
    def __mds(self, dataset):
        """
        Applies classical multidimensional scaling over a
        geodesic distance matrix, and returns
        the coordinates of the low-dimensional mapped points y_1 ... y_n
        """
        numpoints = np.size(dataset, 0)
        squared_proximity_matrix = np.square(dataset)
        double_centered = self.__double_centering(squared_proximity_matrix, numpoints)
        eigenvalues, eigenvectors = eigs(double_centered, k=self.m)
        length = np.diag(eigenvalues)
        y = eigenvectors @ np.sqrt(length)
        return np.real(y)
    
    def __double_centering(self, squared, numpoints):
        """
        Performs double centering using centering matrix j, where n is the number of datapoints
        """
        identity_matrix = np.identity(numpoints)
        ones = np.ones(squared.shape)
        j = identity_matrix - (1 / numpoints) * ones
        b = -(1/2) * j @ squared @ j
        return b
